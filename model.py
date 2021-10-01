import numpy as np
import tensorflow as tf
from tensorflow.keras import layers



def get_angles(pos, i, d_model):
    angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
    return pos * angle_rates


def positional_encoding(position, d_model):
    angle_rads = get_angles( np.arange(position)[:, np.newaxis], np.arange(d_model)[np.newaxis, :], d_model)
    
    # apply sin to even indices in the array; 2i
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    
    # apply cos to odd indices in the array; 2i+1
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    pos_encoding = angle_rads[np.newaxis, ...]
    return tf.cast(pos_encoding, dtype=tf.float32)


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.2):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
    

class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions
    
def lambdaLayerFunction(tensor):
    scalars = inputs_2
    vectors = tensor
    result = tf.convert_to_tensor([tf.scalar_mul(s , v) for (s,v) in zip(scalars, vectors)])
    return result

class ARM(tf.keras.Model):
    def __init__(self, snip_len, embed_dim, num_heads, ff_dim, dropout, vocab_size):
        super(ARM, self).__init__()
        self.embedding_layer = TokenAndPositionEmbedding(snip_len, vocab_size, embed_dim)
        self.transformer = TransformerBlock(embed_dim, num_heads, ff_dim)
        self.pooling = layers.GlobalAveragePooling1D(data_format='channels_first')
        self.dropout = layers.Dropout(dropout)
        self.output_layer = layers.Dense(snip_len, activation = 'sigmoid')
        
    def call(self, inputs):
        y = self.embedding_layer(inputs[0])
        input1 = tf.cast(inputs[1][:,:,tf.newaxis], tf.float32)
        x = tf.multiply(input1, y)
        
        x = self.transformer(x)
        x = x+y
        
        x = self.pooling(x)
        x = self.dropout(x)
        
        x = self.output_layer(x)
        
        return(x)
    
