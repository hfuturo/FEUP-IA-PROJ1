import draw

if __name__ == "__main__":
    while True:
        menu = draw.MainMenu()
        level = menu.run()
        if level is None:
            break

        draw.Game(level)


        
