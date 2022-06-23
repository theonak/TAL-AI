from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense, Reshape, ReLU, Dropout, Input, Flatten
import tensorflow as tf
from champs import NB_CHAMP





def make_dense_model(input_shape = (20,161), layers = [128,64]) :
    model = Sequential([
        Input(shape=input_shape),
        Flatten()
    ])
    if len(input_shape) == 3 :
        model.add(Flatten())
    for layer in layers :
        model.add(Dense(layer, activation="ReLU"))
        model.add(Dropout(0.2))
    model.add(Dense(1, activation=tf.keras.activations.sigmoid))
    model.compile(optimizer='adam', 
                loss= tf.keras.losses.CategoricalCrossentropy(),
                metrics= ["Accuracy"])
    return model



class Sampling(tf.keras.layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

latent_dim = 10

def make_encoder():

    encoder_inputs = tf.keras.Input(shape=(4,NB_CHAMP,))

    x = tf.keras.layers.Flatten()(encoder_inputs)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.1)(x)
    z_mean = tf.keras.layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = tf.keras.layers.Dense(latent_dim, name="z_log_var")(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = tf.keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")
    return encoder

def make_decoder():
    latent_inputs = tf.keras.Input(shape=(latent_dim,))
    x = tf.keras.layers.Dense(128, activation="relu")(latent_inputs)
    x = tf.keras.layers.Dropout(0.1)(x)
    x = tf.keras.layers.Dense(4*NB_CHAMP, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.1)(x)
    decoder_outputs = tf.keras.layers.Dense(NB_CHAMP, activation="sigmoid")(x)
    decoder = tf.keras.Model(latent_inputs, decoder_outputs, name="decoder")
    return decoder


class VAE(tf.keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = tf.keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = tf.keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = tf.keras.metrics.Mean(name="kl_loss")
        self.accuracy_tracker = tf.keras.metrics.CategoricalAccuracy()

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        ((team, champ),) = data
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(team)
            reconstruction = self.decoder(z)
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    tf.keras.losses.categorical_crossentropy(champ, reconstruction)
                )
            )
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + kl_loss


        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        self.accuracy_tracker.update_state(champ,tf.one_hot(tf.math.argmax(reconstruction,1),NB_CHAMP))
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
            "accuracy":self.accuracy_tracker.result()
        }
        
