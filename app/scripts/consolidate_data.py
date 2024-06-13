import os
import io

def consolidate_data(image_file_paths, results_list, image_classification):
    # Zip the four lists together to create a list of tuples
    consolidated_data = list(zip(image_file_paths, results_list, image_classification))
    # Return the consolidated data
    return consolidated_data