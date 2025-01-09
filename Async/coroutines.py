import asyncio

async def fetch_data(delay):
    print("Fetching Data")
    asyncio.sleep(delay)
    print("Data Fetched")
    return{"data":"Some data"}

async def main():
    print("Start of main Coroutine")
    task=fetch_data(2) #This only returns a coroutine object , but still it didn't get executed [creation of a coroutine object]

    result=await task #with the help of await the coroutine object gets executed!
    #we wait for the awaited taks to finish, before we moving on to the rest of the program!
    print(f"Received result:{result}")
    print("End of main coroutine")

asyncio.run(main())