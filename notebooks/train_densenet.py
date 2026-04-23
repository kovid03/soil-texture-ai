"""
Train DenseNet121 on real soil images (555 images, 5 classes).
Uses transfer learning with fine-tuning and heavy data augmentation.

Dataset source: https://github.com/Phantom-fs/Soil-Classification-Dataset
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import json
import numpy as np

# ─── Paths ────────────────────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset', 'train')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

# ─── Hyperparameters ──────────────────────────────────────────────────
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = 25
NUM_CLASSES = 5

# ─── Data Augmentation ───────────────────────────────────────────────
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.25,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.7, 1.3],
    channel_shift_range=20,
    validation_split=0.2,
    fill_mode='nearest'
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    seed=42
)

val_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    seed=42
)

print(f"\nTraining samples:   {train_gen.samples}")
print(f"Validation samples: {val_gen.samples}")
print(f"Classes: {train_gen.class_indices}\n")

# ─── Handle class imbalance with class weights ───────────────────────
from collections import Counter
counter = Counter(train_gen.classes)
total = sum(counter.values())
class_weights = {cls: total / (len(counter) * count) for cls, count in counter.items()}
print(f"Class weights: {class_weights}\n")

# ─── Build Model ─────────────────────────────────────────────────────
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze early layers, fine-tune last 50 layers
for layer in base_model.layers[:-50]:
    layer.trainable = False
for layer in base_model.layers[-50:]:
    layer.trainable = True

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

trainable = sum(1 for l in model.layers if l.trainable)
total_layers = len(model.layers)
print(f"Model: {total_layers} layers, {trainable} trainable\n")

# ─── Callbacks ────────────────────────────────────────────────────────
checkpoint_path = os.path.join(MODEL_DIR, 'soil_densenet.keras')
callbacks = [
    EarlyStopping(patience=8, monitor='val_loss', restore_best_weights=True, verbose=1),
    ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
]

# ─── Train ────────────────────────────────────────────────────────────
print("=== Starting Training ===\n")
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks,
    class_weight=class_weights
)

# ─── Save class mapping ──────────────────────────────────────────────
class_indices = train_gen.class_indices
class_mapping = {str(v): k for k, v in class_indices.items()}
mapping_path = os.path.join(MODEL_DIR, 'class_mapping.json')
with open(mapping_path, 'w') as f:
    json.dump(class_mapping, f, indent=2)

print(f"\nModel saved to:   {checkpoint_path}")
print(f"Mapping saved to: {mapping_path}")
print(f"Class mapping: {class_mapping}")

# ─── Results ──────────────────────────────────────────────────────────
best_val_acc = max(history.history.get('val_accuracy', [0]))
best_train_acc = max(history.history.get('accuracy', [0]))
print(f"\nBest training accuracy:   {best_train_acc:.4f}")
print(f"Best validation accuracy: {best_val_acc:.4f}")
print("\n=== Training Complete ===")
