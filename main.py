import draw

if __name__ == "__main__":
    while True:
        menu = draw.MainMenu()
        level = menu.run()
        if level is None:
            break

        game = draw.Game(level)
        ret = game.run()
        if ret is None:
            break


        
