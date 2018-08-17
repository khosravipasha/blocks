import numpy as np
import scipy as sp

def get_pertubations(indexed_string,
                                num_samples,
                                distance_metric = 'cosine'):
        """
        Generates neighborhood data by randomly removing words from
        the instance. At most removes 2/3 of the text.

        Args:
            indexed_string: document (IndexedString) to be explained,
            num_samples: size of the neighborhood to learn the linear model
            distance_metric: the distance metric to use for sample weighting,
                defaults to cosine similarity
        Returns:
                data: dense num_samples * K binary matrix, where K is the
                    number of tokens in indexed_string. The first row is the
                    original instance, and thus a row of ones.

        """
        doc_size = indexed_string.num_words()
        sample = np.random.randint(1, 2 * doc_size / 3, num_samples - 1)
        data = np.ones((num_samples, doc_size))
        data[0] = np.ones(doc_size)
        features_range = range(doc_size)
        inverse_data = [indexed_string.raw_string()]
        for i, size in enumerate(sample, start=1):
            inactive = np.random.choice(features_range, size, replace=False)
            data[i, inactive] = 0
            inverse_data.append(indexed_string.inverse_removing(inactive))

        return data
