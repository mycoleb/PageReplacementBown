

# I am importing the ABC module to create abstract base classes and the random module to generate random numbers
from abc import ABC, abstractmethod
import random
import unittest
from page_replacement import FIFOReplacementAlgorithm, LRUReplacementAlgorithm, OPTReplacementAlgorithm

# I am defining an abstract base class called ReplacementAlgorithm
class ReplacementAlgorithm(ABC):
    # I am initializing my ReplacementAlgorithm with the number of page frames
    def __init__(self, page_frame_count):
        # I am checking if the page frame count is negative and raising an error if it is
        if page_frame_count < 0:
            raise ValueError("Page frame count cannot be negative")
        # I am storing the page frame count
        self.page_frame_count = page_frame_count
        # I am initializing the page fault count to zero
        self.page_fault_count = 0
        # I am initializing an empty list to keep track of page frames
        self.page_frames = []

    # I am defining a method to get the current page fault count
    def get_page_fault_count(self):
        return self.page_fault_count

    # I am declaring an abstract method insert that must be implemented by subclasses
    @abstractmethod
    def insert(self, page_number):
        pass

# I am defining a class for the FIFO page replacement algorithm that inherits from ReplacementAlgorithm
class FIFOReplacementAlgorithm(ReplacementAlgorithm):
    # I am implementing the insert method for the FIFO algorithm
    def insert(self, page_number):
        # I am checking if the page is not already in memory
        if page_number not in self.page_frames:
            # I am incrementing the page fault count since the page is not in memory
            self.page_fault_count += 1
            # I am checking if the number of pages in memory exceeds the page frame count
            if len(self.page_frames) >= self.page_frame_count:
                # I am removing the oldest page from memory
                self.page_frames.pop(0)
            # I am adding the new page to memory
            self.page_frames.append(page_number)

# I am defining a class for the LRU page replacement algorithm that inherits from ReplacementAlgorithm
class LRUReplacementAlgorithm(ReplacementAlgorithm):
    # I am implementing the insert method for the LRU algorithm
    def insert(self, page_number):
        # I am checking if the page is not already in memory
        if page_number not in self.page_frames:
            # I am incrementing the page fault count since the page is not in memory
            self.page_fault_count += 1
            # I am checking if the number of pages in memory exceeds the page frame count
            if len(self.page_frames) >= self.page_frame_count:
                # I am removing the oldest page from memory
                self.page_frames.pop(0)
            # I am adding the new page to memory
            self.page_frames.append(page_number)
        else:
            # I am updating the position of the page since it is accessed again
            self.page_frames.remove(page_number)
            self.page_frames.append(page_number)

# I am defining a class for the OPT page replacement algorithm that inherits from ReplacementAlgorithm
class OPTReplacementAlgorithm(ReplacementAlgorithm):
    # I am implementing the insert method for the OPT algorithm
    def insert(self, page_number, future_references):
        # I am checking if the page is not already in memory
        if page_number not in self.page_frames:
            # I am incrementing the page fault count since the page is not in memory
            self.page_fault_count += 1
            # I am checking if the number of pages in memory exceeds the page frame count
            if len(self.page_frames) >= self.page_frame_count:
                # I am finding the page in memory that will not be used for the longest period of time
                furthest_use = -1
                page_to_remove = -1
                for frame in self.page_frames:
                    if frame not in future_references:
                        page_to_remove = frame
                        break
                    else:
                        next_use = future_references.index(frame)
                        if next_use > furthest_use:
                            furthest_use = next_use
                            page_to_remove = frame
                # I am removing the page that will not be used for the longest time
                self.page_frames.remove(page_to_remove)
            # I am adding the new page to memory
            self.page_frames.append(page_number)

# I am defining a function to run a given page replacement algorithm with a reference string and return the number of page faults
def run_algorithm(algorithm_class, reference_string, page_frame_count, future_references=None):
    # I am creating an instance of the specified algorithm class
    algorithm = algorithm_class(page_frame_count)
    # I am iterating over the reference string
    for i, page_number in enumerate(reference_string):
        # I am checking if future references are provided (for OPT algorithm)
        if future_references:
            # I am inserting the page number with future references
            algorithm.insert(page_number, future_references[i+1:])
        else:
            # I am inserting the page number without future references
            algorithm.insert(page_number)
    # I am returning the number of page faults
    return algorithm.get_page_fault_count()

# I am defining a function to generate a random reference string of a given length
def generate_random_reference_string(length):
    # I am returning a list of random page numbers between 0 and 9
    return [random.randint(0, 9) for _ in range(length)]

# I am defining the main function to run the experiments
def main():
    # I am defining the given reference strings
    reference_strings = [
        [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1],
        [8,1,0,7,3,0,3,4,5,3,5,2,0,6,8,4,8,1,5,3],
        [4,6,4,8,6,3,6,0,5,9,2,1,0,4,6,3,0,6,8,4]
    ]

    # I am defining the configurations to test with different lengths and frame counts
    configurations = [
        (15, 3),
        (15, 5),
        (15, 7)
    ]

    # I am iterating over the given reference strings to test the algorithms
    for reference_string in reference_strings:
        # I am printing the reference string
        print("Reference String:", reference_string)
        # I am running the FIFO algorithm and printing the page fault count
        print("FIFO:", run_algorithm(FIFOReplacementAlgorithm, reference_string, 3))
        # I am running the LRU algorithm and printing the page fault count
        print("LRU:", run_algorithm(LRUReplacementAlgorithm, reference_string, 3))
        # I am running the OPT algorithm and printing the page fault count
        print("OPT:", run_algorithm(OPTReplacementAlgorithm, reference_string, 3, future_references=reference_string))

    # I am iterating over the configurations to test with random reference strings
    for length, frames in configurations:
        # I am generating a random reference string
        reference_string = generate_random_reference_string(length)
        # I am printing the random reference string
        print("\nRandom Reference String:", reference_string)
        # I am printing the configuration details
        print(f"Configuration: Length={length}, Frames={frames}")
        # I am running the FIFO algorithm and printing the page fault count
        print("FIFO:", run_algorithm(FIFOReplacementAlgorithm, reference_string, frames))
        # I am running the LRU algorithm and printing the page fault count
        print("LRU:", run_algorithm(LRUReplacementAlgorithm, reference_string, frames))
        # I am running the OPT algorithm and printing the page fault count
        print("OPT:", run_algorithm(OPTReplacementAlgorithm, reference_string, frames, future_references=reference_string))

# I am checking if this script is being run directly
if __name__ == "__main__":
    # I am calling the main function to execute the program
    main()

#I really hope this is what you meant by PyUnit tests

class TestPageReplacementAlgorithms(unittest.TestCase):
    def test_fifo_algorithm(self):
        # Test case 1
        algorithm = FIFOReplacementAlgorithm(3)
        reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        for page in reference_string:
            algorithm.insert(page)
        self.assertEqual(algorithm.get_page_fault_count(), 15)

        # Test case 2
        algorithm = FIFOReplacementAlgorithm(4)
        reference_string = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]
        for page in reference_string:
            algorithm.insert(page)
        self.assertEqual(algorithm.get_page_fault_count(), 10)

    def test_lru_algorithm(self):
        # Test case 1
        algorithm = LRUReplacementAlgorithm(3)
        reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        for page in reference_string:
            algorithm.insert(page)
        self.assertEqual(algorithm.get_page_fault_count(), 12)

        # Test case 2
        algorithm = LRUReplacementAlgorithm(4)
        reference_string = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]
        for page in reference_string:
            algorithm.insert(page)
        self.assertEqual(algorithm.get_page_fault_count(), 10)

    def test_opt_algorithm(self):
        # Test case 1
        reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        algorithm = OPTReplacementAlgorithm(3)
        for i, page in enumerate(reference_string):
            algorithm.insert(page, reference_string[i+1:])
        self.assertEqual(algorithm.get_page_fault_count(), 9)

        # Test case 2
        reference_string = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]
        algorithm = OPTReplacementAlgorithm(4)
        for i, page in enumerate(reference_string):
            algorithm.insert(page, reference_string[i+1:])
        self.assertEqual(algorithm.get_page_fault_count(), 8)

if __name__ == '__main__':
    unittest.main()