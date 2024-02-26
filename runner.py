import dtlpy as dl
import logging

from dlgetty import GettySession

logger = logging.getLogger('[GETTY]')


class ServiceRunner(dl.BaseServiceRunner):

    def __init__(self):
        self.session = GettySession(runner=self)

    def search_and_add_images(self, dataset: dl.Dataset, phrase=None, n_images=10):
        """
        Inflate dataset with items from getty
        :param dataset: dataset to inflate
        :param phrase: phrase to search in getty
        :param n_images: number of images to upload
        :return:
        """
        self.session.run(dataset=dataset, search_phrase=phrase, n_images=n_images)


def test():
    dl.setenv('prod')
    service_runner = ServiceRunner()
    service_runner.search_and_add_images(dataset=dl.datasets.get(dataset_id='65c37569453b7f942b2e7b1f'),
                                         phrase="coconut",
                                         n_images=20)


if __name__ == "__main__":
    test()
