from Server import Server

if __name__ == '__main__':
    while True:
        try:
            s = Server()
            s.start()
        except BaseException as e:
            print("[ERROR] {}".format(str(e)))

