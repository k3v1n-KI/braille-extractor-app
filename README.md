# braille-extractor-app
This app is designed to convert different types of content to braille. Here are the complete sets of features this application has:
- Image to Braille, English and Audio Converter
- Speech to Text and Braille Converter
- Braille to English Text Converter
- English to Braille Text Converter

### Setting up
In order to run the application, you need to setup the virual environment and install all the requirements

If you do not have Virtual Environment installed install it using the following command:

```bash
$ ~ pip install virtualenv
```

After virtual environment is available in your system create and activate the virtual environment using the following commands.

> Make sure to be in the app folder before creating the virtual environment


```bash
$ braille-extractor-app> python -m venv braille-extractor-app
$ braille-extractor-app> source ./braille-extractor-app/bin/activate
$ braille-extractor-app (braille-extractor-app) >

```

As seen in the last line above, there will be an indication on the command line that the virtual environment is active. Once that is done, proceed to install the requirements using the following command.

```bash
$ braille-extractor-app (braille-extractor-app) > pip install -r requirements.txt

```

This will install all the required packages to run the application server.

> Please note that you must also install an application called 'ffmpeg' for speech to text conversion. You can find the instructions [here](https://ffmpeg.org/download.html). Application will still run but you might face issues during speech conversion. You might also need to change the directory for ffmpeg executable in `main.py` line 16.


### Running the server

Once the server setup is ready, you can run the application by running the `main.py` file using the following command.

```bash
$ braille-extractor-app (braille-extractor-app) > python main.py
```

Now access the web application on a web browser using the following url: [http://localhost:5000](ttp://localhost:5000)
