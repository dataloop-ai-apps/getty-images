import dtlpy as dl
import logging

from dlgetty import GettySession

logger = logging.getLogger('[GETTY]')


class ServiceRunner(dl.BaseServiceRunner):

    def __init__(self):
        self.session = GettySession(runner=self)

    def search_and_add_images(self, dataset: dl.Dataset, search_phrase=None, number_of_images=10):
        """
        Inflate dataset with items from getty
        :param dataset: dataset to inflate
        :param search_phrase: phrase to search in getty
        :param number_of_images: number of images to upload
        :return:
        """
        self.session.run(dataset=dataset, search_phrase=search_phrase, n_images=number_of_images)


def test():
    dl.setenv('prod')
    service_runner = ServiceRunner()
    service_runner.search_and_add_images(dataset=dl.datasets.get(dataset_id='65c37569453b7f942b2e7b1f'),
                                         search_phrase="coconut",
                                         number_of_images=20)


if __name__ == "__main__":
    test()
