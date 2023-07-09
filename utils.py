from database import Datasets


def save_images(images, dataset_name):
    dataset = Datasets()
    dataset.add_images_to_dataset(images, dataset_name)


def get_preview_images(dataset_name, count=10, idx=0, max_count=None):
    dataset = Datasets()
    return dataset.get_dataset(dataset_name, count, idx, max_count)


def get_dataset_names():
    dataset = Datasets()
    return dataset.collection.find().distinct('dataset_name')


def total_image_count(dataset_name):
    dataset = Datasets()
    return dataset.collection.count_documents({"dataset_name": dataset_name})


def save_images_to_dataset(images):
    dataset = Datasets()
    return dataset.add_images_to_dataset(images)
