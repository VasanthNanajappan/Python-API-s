import asyncio

async def fetch_data(id,sleep_time):
    print(f"Coroutine {id} starting o fetch data.")
    await asyncio.sleep(sleep_time)
    return {"id":id,"data":f"Sample data from coroutine {id}"}

async def main():
    #creating tasks to run coroutines concurrently
    task1=asyncio.create_task(fetch_data(1,2))
    task2=asyncio.create_task(fetch_data(2,3))
    task3=asyncio.create_task(fetch_data(3,1))

    result1=await task1
    result2=await task2
    result3=await task3

    print(result1,result2,result3)

asyncio.run(main())

#gather() function is used to create/concurrently running multiple coroutines
#result= await asyncio.gather(fetch_data(1,2),fetch_data(2,3),fetch_data(3,1))


#task group - it is similiar as gather() function and it provides Built-in Error Handling
#future - it is a promise of a future result. Result is going to come in future, we don't know when it comes
