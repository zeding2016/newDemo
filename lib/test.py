# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/9/27'
import asyncio
import time


# 单个任务的
async def work1(x):
    await asyncio.sleep( x )
    print( "work{}".format( x ) )
    return (x * x)


def callback(x):
    print( "我是回调函数:{}".format( str( x ) ) )







# demo 1  create_task
# a = work1(5)
# co = asyncio.get_event_loop()
# task = co.create_task(a)
# # assert isinstance(task, asyncio.Task)
# #绑定回调函数
# task.add_done_callback(callback)
# co.run_until_complete(task)
# print(task.result())
#
#
#--------------------------------------------
#--------------------------------------------


# demo2  ensure_future
# a = work1(6)
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(a)
# loop.run_until_complete(task)
# print (task.result())

#--------------------------------------------
#--------------------------------------------



# demo3
# tasks=[
#     asyncio.ensure_future(work1(1)),
#     asyncio.ensure_future( work1( 12) ),
#     asyncio.ensure_future( work1( 5 ) ),
#     asyncio.ensure_future( work1( 10) )
#
# ]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
#
# for t in tasks:
#     print(t.result())
#
#--------------------------------------------
#--------------------------------------------

# demo4 增加回调函数
#
# tasks=[
#     asyncio.ensure_future(work1(1)),
#     asyncio.ensure_future( work1( 12) ),
#     asyncio.ensure_future( work1( 5 ) ),
#     asyncio.ensure_future( work1( 10) )
#
# ]
# for i in tasks:
#    i.add_done_callback( callback )
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))

#--------------------------------------------
#--------------------------------------------

# demo5 协程嵌套
# async def main():
#     tasks=[
#         asyncio.ensure_future(work1(1)),
#         asyncio.ensure_future( work1( 12) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10) )
#
#     ]
#     for i in tasks:
#        i.add_done_callback( callback )
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait(tasks))
#
#
#
# main()
#--------------------------------------------
#--------------------------------------------


# demo6 协程嵌套
# async def main():
#     tasks = [
#         asyncio.ensure_future( work1( 1 ) ),
#         asyncio.ensure_future( work1( 12 ) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10 ) )
#
#     ]
#     dones, pendings = await asyncio.wait( tasks )
#
#     for i in dones:
#         print(i.result())
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

#--------------------------------------------
#--------------------------------------------

# demo7 协程嵌套 如果使用的是 asyncio.gather创建协程对象，那么await的返回值就是协程运行的结果
# async def main():
#     tasks = [
#         asyncio.ensure_future( work1( 1 ) ),
#         asyncio.ensure_future( work1( 12 ) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10 ) )
#
#     ]
#
#     return await asyncio.gather( *tasks )
#
# loop = asyncio.get_event_loop()
# r = loop.run_until_complete(main())
# for i in r:
#     print(i)
#--------------------------------------------



#--------------------------------------------

#demo8 返回使用asyncio.wait方式挂起协程。
# async def main():
#     tasks = [
#         asyncio.ensure_future( work1( 1 ) ),
#         asyncio.ensure_future( work1( 12 ) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10 ) )
#
#     ]
#
#     return await asyncio.wait(tasks)
# loop = asyncio.get_event_loop()
# r ,b= loop.run_until_complete(main())
#
# for i in r:
#     print(i.result())
#

# --------------------------------------------

#--------------------------------------------
#demo9 也可以使用asyncio的as_completed方法,这个方法比较好
# t = None
# async def main():
#     global t
#     tasks = [
#         asyncio.ensure_future( work1( 1 ) ),
#         asyncio.ensure_future( work1( 12 ) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10 ) )
#
#     ]
#     for task in asyncio.as_completed( tasks ):
#         result = await task
#         if(result==25):
#             t = result
#         print( 'Task ret: {}'.format( result ) )
#
# loop = asyncio.get_event_loop()
# done = loop.run_until_complete( main() )
#
# print(t)

#--------------------------------------------
#--------------------------------------------
#demo10 上面见识了协程的几种常用的用法，都是协程围绕着事件循环进行的操作。future对象有几个状态：
    #
    # Pending
    # Running
    # Done
    # Cancelled
#
# tasks = [
#         asyncio.ensure_future( work1( 1 ) ),
#         asyncio.ensure_future( work1( 12 ) ),
#         asyncio.ensure_future( work1( 5 ) ),
#         asyncio.ensure_future( work1( 10 ) )
#
#     ]
#
# for i in tasks:
#     i.add_done_callback(callback)
#
#
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(asyncio.wait(tasks))
# except KeyboardInterrupt as e:
#     for i in tasks:
#         try:
#             if(i.result()):
#                 print(i,"######")
#         except Exception as r:
#             pass
#
#     print(asyncio.Task.all_tasks())
#     for task in asyncio.Task.all_tasks():
#         print(task.cancel())
#     loop.stop()
#     loop.run_forever()
# finally:
#     loop.close()
#
#


#--------------------------------------------
#--------------------------------------------
#demo11'
# async  def main():
#     tasks = [
#             asyncio.ensure_future( work1( 1 ) ),
#             asyncio.ensure_future( work1( 12 ) ),
#             asyncio.ensure_future( work1( 5 ) ),
#             asyncio.ensure_future( work1( 10 ) )]
#
#
#     dones, pendings = await asyncio.wait( tasks )
#     for task in dones:
#         print( 'Task ret: ', task.result() )
#
#
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
# except KeyboardInterrupt as keyInter:
#     stop=[]
#     dloop = asyncio.new_event_loop()
#     for i in asyncio.Task.all_tasks():
#         if(i.cancel()):
#             stop.append(i)
#         else:
#             print("已经运行")
#
#     for j in stop:
#         j.add_done_callback(callback)
#
#
#     dloop.run_until_complete(asyncio.wait(stop))
#     dloop.close()
#     # print( asyncio.gather( *asyncio.Task.all_tasks() ).cancel() )
#     loop.stop()
#     loop.run_forever()
# finally:
#     loop.close()



#--------------------------------------------
#--------------------------------------------
#demo12  很多时候，我们的事件循环用于注册协程，而有的协程需要动态的添加到事件循环中
    #。  一个简单的方式就是使用多线程。当前线程创建一个事件循环，然后在新建一个线程，
    #   在新线程中启动事件循环。当前线程不会被block。

#
# from threading import Thread
#
#
# def start_loop(loop):
#     asyncio.set_event_loop( loop )
#     loop.run_forever()
#
#
# def more_work(x):
#     print( 'More work {}'.format( x ) )
#     time.sleep( x )
#     print( 'Finished more work {}'.format( x ) )
#
#
#
# new_loop = asyncio.new_event_loop()
# t = Thread( target=start_loop, args=(new_loop,) )
# t.start()
#
#
# new_loop.call_soon_threadsafe( more_work, 6 )
# new_loop.call_soon_threadsafe( more_work, 3 )
#


#--------------------------------------------
#--------------------------------------------
#demo13 新线程协程
from threading import Thread

def mian_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
  
  
    
async def work(x):
    print("work 开始等待{}".format(x))
    await asyncio.sleep(x)
    print("work 结束{}".format(x))




def otherWork(x):
    print( "otherWork 开始等待{}".format( x ) )
    time.sleep( x )
    print( "otherWork 结束{}".format( x ) )

s = time.time()

new_loop = asyncio.new_event_loop()
t = Thread(target=mian_loop,args=(new_loop,))
t.start()
n =0




while True:
    time.sleep(10)
    n +=1
    asyncio.run_coroutine_threadsafe(work(2),new_loop)
    asyncio.run_coroutine_threadsafe( work( 6 ), new_loop )
   


