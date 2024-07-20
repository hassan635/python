from ascii_magic import AsciiArt, Back, Front
import glob


if __name__ == "__main__":
    
    my_art = AsciiArt.from_image('./images/subscribe8.png')
    my_output = my_art.to_ascii(columns=180, front=Front.GREEN, back=Back.BLACK)
    print(my_output)
    
    #my_art = AsciiArt.from_image('./images/luffy.png')
    #my_art.to_html_file('thumb.html', columns=200, width_ratio=2, additional_styles='color: green;')
    
    
    #AsciiArt.to_html_file('./images/luffy.png', columns=200)
    #AsciiArt.from_image("./images/subscribe4.png").to_terminal()
    #AsciiArt.from_image("./images/luffyPoster.jpg").to_terminal()
    
    
    """ images = []
    for image in glob.glob("./images/*"):
        images.append(image)
    
    for image in images:
        my_art = AsciiArt.from_image(image)
        my_art.to_terminal()
        print("\n\n") """

