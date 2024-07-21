from ascii_magic import AsciiArt, Back, Front
import glob
import os

if __name__ == "__main__":
    '''
    This scripts takes in an input image from the 
    local directory and uses the Ascii Magic library
    to output an Ascii art equivalent in an html file.
    '''
    input_image = AsciiArt.from_image('./images/shanks.jpeg')
    output_file_name = 'art.html'
    input_image.to_html_file(output_file_name, columns=200, width_ratio=2)
    print(os.path.abspath(output_file_name))

