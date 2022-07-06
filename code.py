class Stoneview(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
      #  pdb.set_trace()
        import datetime
        from datetime import timezone
        
        dt = datetime.datetime.now(timezone.utc)
        
        utc_time = dt.replace(tzinfo=timezone.utc)
      #  print(utc_time)
        utc_timestamp = utc_time.timestamp()
        
        showtime1 = datetime.datetime.now()
        time1 = showtime1.replace(second=0,microsecond=0)
        time2 = showtime1.replace(minute=showtime1.minute+1,second=0,microsecond=0)
        client = FivePaisaClient(email=login_cred["email"],passwd=login_cred["passwd"],dob=login_cred["dob"],cred=cred)
        client.login() 

        dict1 =  {"Exchange":"N","ExchangeType":"C","ScripCode":"999920000"}        
        a = [dict1]
        k=client.fetch_market_depth(a)
       # print(k)
        last_value = k["Data"][0]["LastTradedPrice"]
        print(last_value)

        from time import gmtime, strftime
       # from datetime import datetime
     #   showtime1 = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
      #  showtime1 = datetime.now()

        cache_data = redis.StrictRedis()
        try:
            stored_time = eval(cache_data.get("time"))["time"]
            stored_open = float(cache_data.get("open").decode())
            stored_high = float(cache_data.get("high").decode())
            stored_low = float(cache_data.get("low").decode())
            stored_close = float(cache_data.get("close").decode())
            if stored_time.minute != showtime1.minute:
                stored_time = datetime.datetime.now()

                cache_data.set("time",str({"time":stored_time}))
                #stored_open = last_value ##
                if time2 >= showtime1 and time1 <= showtime1:
                    stored_open = last_value
                    cache_data.set("open",stored_open)
                    # stored_high = last_value ##
                    # cache_data.set("high",stored_high)
                    # stored_low = last_value
                    # cache_data.set("low",stored_low)
                else:
                    stored_close = last_value
                    cache_data.set("close",stored_close)
                    # stored_high = last_value ##
                    # cache_data.set("high",stored_high)
                    # stored_low = last_value
                    # cache_data.set("low",stored_low)
               # open = last_value  # maybe close also
             #   cache_data.set("open",open)
                if last_value > stored_high:
                    cache_data.set("high",last_value)
                    stored_high = last_value
                if last_value < stored_low:
                    cache_data.set("low",last_value)
                    stored_low = last_value
                ret_dict = {
                    "status": True,
                    "time": utc_timestamp,
                    "open": stored_open,
                    "high": stored_high,
                    "low" : stored_low,
                    "close": stored_close
                }
                print(ret_dict)
                return Response(ret_dict, status.HTTP_200_OK)
            else:
                if last_value > stored_high:
                    cache_data.set("high",last_value)
                    stored_high = last_value
                if last_value < stored_low:
                    cache_data.set("low",last_value)
                    stored_low = last_value
                ret_dict = {
                    "status": False,
                    "time":utc_timestamp,
                    "open": stored_open,
                    "high": stored_high,
                    "low" : stored_low,
                    "close": stored_close
                }
                print(ret_dict)
                return Response(ret_dict, status.HTTP_200_OK)


        except:
            cache_data.set("time",str({"time":datetime.datetime.now()}))
            cache_data.set("open",last_value)
            cache_data.set("high",last_value)
            cache_data.set("low",last_value)
            cache_data.set("close",last_value)
