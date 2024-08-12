# Импорт необходимых библиотек
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# Загрузка данных CIFAR-10
cifar10 = tf.keras.datasets.cifar10
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Преобразование значений пикселей в диапазон 0-1 для нормализации данных
train_images, test_images = train_images / 255.0, test_images / 255.0

# Названия классов для датасета CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# Визуализация нескольких примеров изображений из обучающего набора
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])  # Убираем отметки по оси x
    plt.yticks([])  # Убираем отметки по оси y
    plt.grid(False)  # Убираем сетку
    plt.imshow(train_images[i])  # Отображаем изображение в цвете
    plt.xlabel(class_names[train_labels[i][0]])  # Подписываем изображения названиями классов
plt.show()

# Создание модели нейронной сети
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),  # Первый сверточный слой с 32 фильтрами и активацией ReLU
    layers.MaxPooling2D((2, 2)),  # Первый слой подвыборки (пулинг) с окном 2x2
    layers.Conv2D(64, (3, 3), activation='relu'),  # Второй сверточный слой с 64 фильтрами и активацией ReLU
    layers.MaxPooling2D((2, 2)),  # Второй слой подвыборки (пулинг) с окном 2x2
    layers.Conv2D(64, (3, 3), activation='relu'),  # Третий сверточный слой с 64 фильтрами и активацией ReLU
    layers.Flatten(),  # Преобразуем выходы сверточных слоев в одномерный вектор
    layers.Dense(64, activation='relu'),  # Полносвязный слой с 64 нейронами и активацией ReLU
    layers.Dense(10, activation='softmax')  # Выходной слой с 10 нейронами и активацией Softmax для классификации на 10 классов
])

# Вывод архитектуры модели
model.summary()

# Компиляция модели с оптимизатором Adam, функцией потерь sparse_categorical_crossentropy и метрикой accuracy
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Обучение модели на обучающем наборе данных
history = model.fit(train_images, train_labels, epochs=15, validation_data=(test_images, test_labels))

# Построение графиков точности обучения и валидации
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

# Предсказание классов для тестовых изображений
predictions = model.predict(test_images)

# Визуализация нескольких предсказаний
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])  # Убираем отметки по оси x
    plt.yticks([])  # Убираем отметки по оси y
    plt.grid(False)  # Убираем сетку
    plt.imshow(test_images[i])  # Отображаем изображение в цвете
    predicted_label = np.argmax(predictions[i])  # Предсказанный класс
    true_label = test_labels[i][0]  # Истинный класс
    if predicted_label == true_label:
        color = 'blue'  # Если предсказание верно, цвет текста синий
    else:
        color = 'red'  # Если предсказание неверно, цвет текста красный
    plt.xlabel("{} ({})".format(class_names[predicted_label], class_names[true_label]), color=color)  # Подписываем изображения предсказанным и истинным классами
plt.show()
