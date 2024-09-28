import os
import sys
import fitz  # PyMuPDF
import io
from PIL import Image, UnidentifiedImageError
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration
import matplotlib.pyplot as plt
from tabulate import tabulate
import csv  # Import CSV module

# Load the model and processor for DePlot
processor = Pix2StructProcessor.from_pretrained('google/deplot')
model = Pix2StructForConditionalGeneration.from_pretrained('google/deplot')

def main(pdf_dir):
    # Function to perform inference on extracted images
    def inference_on_images(image_paths):
        log_file_path = 'extracted_data.log'  # Name of the log file to save data

        # Open the log file for writing
        with open(log_file_path, mode='w') as log_file:
            log_file.write("Image Name\tExtracted Data\n")  # Write headers to the log file

            for img_path in image_paths:
                try:
                    # Load the image using PIL
                    image = Image.open(img_path)
                    image.verify()  # Check if it's a valid image
                    image = Image.open(img_path)  # Reopen since verify() closes the file
                    
                    # Prepare the input for the model
                    inputs = processor(images=image, text="Generate underlying data table of the figure below:", return_tensors="pt")

                    # Generate predictions
                    predictions = model.generate(**inputs, max_new_tokens=512)

                    # Decode the output and convert it to a table
                    raw_output = processor.decode(predictions[0], skip_special_tokens=True)
                    split_by_newline = raw_output.split("<0x0A>")
                    result_array = []

                    for item in split_by_newline:
                        result_array.append([x.strip() for x in item.split("|")])

                    # Write the extracted table to the log file
                    log_file.write(f"\n---- EXTRACTED TABLE for {img_path} ----\n")
                    for row in result_array:
                        log_file.write(" | ".join(row) + "\n")

                    # Log that the original graph is displayed
                    log_file.write(f"\n---- ORIGINAL GRAPH for {img_path} ----\n")

                    # Display the original graph in the console
                    print('\n---- ORIGINAL GRAPH ----')
                    plt.imshow(image)
                    plt.axis('off')
                    plt.show()
                
                except (UnidentifiedImageError, IOError) as e:
                    print(f"Skipping file {img_path} due to an error: {e}")
                    log_file.write(f"Error processing {img_path}: {e}\n")  # Log any errors


    # Iterate through all PDF files in the specified directory
    extracted_image_paths = []
    for file_name in os.listdir(pdf_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, file_name)
            
            # Open the PDF file
            pdf_file = fitz.open(file_path)

            # Iterate over PDF pages
            for page_index in range(len(pdf_file)):
                # Get the page itself
                page = pdf_file.load_page(page_index)  # load the page
                image_list = page.get_images(full=True)  # get images on the page

                # Printing number of images found in this page
                if image_list:
                    print(f"[+] Found a total of {len(image_list)} images on page {page_index} of {file_name}")
                else:
                    print("[!] No images found on page", page_index, "of", file_name)

                for image_index, img in enumerate(image_list, start=1):
                    # Get the XREF of the image
                    xref = img[0]

                    # Extract the image bytes
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]

                    # Get the image extension
                    image_ext = base_image["ext"]

                    # Save the image
                    image_name = f"{file_name.replace('.pdf', '')}_page{page_index+1}_img{image_index}.{image_ext}"
                    with open(image_name, "wb") as image_file:
                        image_file.write(image_bytes)
                        print(f"[+] Image saved as {image_name}")
                        extracted_image_paths.append(image_name)

            # Close the PDF file
            pdf_file.close()

    # Run inference on all extracted images
    inference_on_images(extracted_image_paths)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_image_extractor.py <pdf_directory>")
        sys.exit(1)

    pdf_directory = sys.argv[1]
    main(pdf_directory)
