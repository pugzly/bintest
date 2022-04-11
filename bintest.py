import websocket, time, json, threading

socket = "wss://stream.binance.com:9443/ws/!ticker@arr"

market_data = []
stayAlive = True


def on_error(ws, error):
    # console print or log (any errors from the binance socket stream thread)
    print("WS Error: ", error)

def on_open(ws):
    # console print or log (new connection from the socket thread)
    print("WS connection opened.")
 
def on_close(ws, close_status_code, close_msg):
    # console print or log closing of binance socket stream thread,
    # and attempt to restart the thread if it should be kept alive
    print("WS Connection closed: ", close_status_code, close_msg)
    if stayAlive:
      print("Will attempt to reconnect in 10 seconds.")
      time.sleep(10)
      print("WS attempting to reconnect...")
      binsocket_thread(socket)

def on_message(ws, payload):
    # convert message payload from binance socket stream to global list variable
    global market_data
    market_data = json.loads(payload)

def binsocket_thread(socket_url):
    # thread for binance socket stream
    websocket.setdefaulttimeout(5)
    ws = websocket.WebSocketApp(socket_url, on_message = on_message, on_close = on_close, on_error = on_error)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = False
    wst.start()


def main():
    binsocket_thread(socket)
    print("Waiting for market data..")
    while len(market_data) < 1: 
       time.sleep(5)

    # get all available pairs in to a list and print out sorted alphabetically
    pairs = []
    for pair in market_data: 
        pairs.append(pair["s"])
    pairs.sort() 

    print("Available pairs:")
    # print only up to 10 elements per line
    pair_index = 0
    for element in pairs:
        print(element, end=" ") 
        if pair_index % 10 == 0: 
            print(element)
        pair_index = pair_index + 1
    print("\n")

    pair_watch = ""
    price_alert = 0.0
    #last_price = 0.0
    while stayAlive:
        time.sleep(2) 

        # check for latest currency pairs   
        new_pairs = []
        for pair in market_data: 
          new_pairs.append(pair["s"])
        new_pairs.sort()

        # make a list of new currency pairs
        only_new = []
        for new in new_pairs:
            if new not in pairs:
                only_new.append(new)

        # print out all the new currency pairs found, and add them to list of all pairs
        if len(only_new) > 0:
            print("! New pairs:")
            for n in only_new:
                print(n, end = " ")
            print("\n")
        pairs = pairs + only_new
        pairs.sort()
         
      
        if pair_watch == "":
            # get user input for currency pair to watch
            pair_watch = input("Enter currency pair to watch: ")
            while pair_watch.upper() not in pairs:
                pair_watch = input("Invalid pair. Enter currency pair to watch: ")

            # print out last price for currency pair we're watching 
            for pair in market_data:
                if pair["s"] == pair_watch.upper(): 
                    last_price = float(pair["c"])
            print("Pair : ", pair_watch.upper(), "  Last price : ", last_price)

            # get user input for max price alert
            price_alert = float(input("Enter max price : "))
            while price_alert <= last_price:
                price_alert = float(input("Price alert price must be higher than last price. Enter new max price : "))

        else:
            for pair in market_data:
                if pair["s"] == pair_watch.upper(): 
                    last_price = float(pair["c"]) 

            if price_alert <= last_price:
                print("!! Pair : ", pair_watch.upper(), " last price ", last_price ," is ABOVE max of ", price_alert, " !!")
            else:
                print("Watching : ", pair_watch.upper(), ", Max price: ", price_alert, " Current price: ", last_price)

        
            
              
if __name__ == "__main__": main()

   





