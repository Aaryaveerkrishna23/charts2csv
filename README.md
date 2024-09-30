# charts2csv
```
Tired of figuring out how to process your proprietary data, like a list of PDFs, on your local VM or computer instead of relying on online websites to convert charts into CSV files and extract insights using state-of-the-art models like LLAVA or GPT-4?

Then, my friend, you have clicked on the right link!

Check out the rest of the GitHub repository to find out how!
```
## Demo

![Demo Image](https://raw.githubusercontent.com/Aaryaveerkrishna23/charts2csv/main/demo2.png)


### README.md

```markdown
# PDF Image Extractor and DePlot Inference

This project extracts images from PDF files and runs inference using the [DePlot](https://huggingface.co/google/deplot) model to generate data tables from graph images. The setup uses Docker and Docker Compose to simplify deployment and make it easy to get started.
```
```
Deplot is a One-shot visual language understanding model that translates images of plots into tables.

```
## Prerequisites
```
- Docker installed on your machine.
- Docker Compose installed on your machine.
- A directory containing the PDF files you want to process.
```

## Directory Structure

Make sure to use the following directory structure:

```
- project/
  - pdf_image_extractor.py
  - Dockerfile
  - requirements.txt
  - docker-compose.yml
  - pdf_files/
    - example1.pdf
    - example2.pdf

```

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd deplot
```

### Step 2: Place Your PDF Files

Add all the PDF files you want to process into the `pdf_files` directory.

### Step 3: Build and Run with Docker Compose

To build the Docker image and run the application, you need to use Docker Compose. If this is your first time running the project, use the following command to **build** the image:

```bash
docker-compose up --build
```

### Step 4: Subsequent Runs

For subsequent runs, you can simply use:

```bash
docker-compose up
```

The `docker-compose up --build` command is needed only when:
- You are running the project for the first time.
- You have made changes to the `Dockerfile` or the requirements, and you need to rebuild the image.

### How It Works

1. The Docker container is built with all the necessary dependencies.
2. When the container runs, it executes the `pdf_image_extractor.py` script.
3. The script extracts images from all PDF files found in the `pdf_files` directory.
4. The DePlot model processes these images to generate data tables and logs it into the directory with a name "extracted_data.log" .

### Output

- Extracted tables are displayed in the console.
- Graphs are displayed as images for visualization.
- Data Extracted in extracted_data.log
  
### Clean Up

To stop the running container, press `Ctrl + C` in your terminal.

To remove the stopped container, you can use:

```bash
docker-compose down
```

### Issues and Troubleshooting

- **Docker Permissions**: Ensure Docker has the necessary permissions to read the `pdf_files` directory.
- **Model Download**: The first time the container runs, the DePlot model will be downloaded, which might take some time.

### Dependencies

- Python 3.9 (used in Docker container)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [Matplotlib](https://matplotlib.org/)
- [Tabulate](https://pypi.org/project/tabulate/)
- [Torch](https://pytorch.org/)

All dependencies are installed automatically inside the Docker container using the `requirements.txt` file.

### Contributing
```
Feel free to fork the repository and make modifications. Pull requests are welcome!
```

