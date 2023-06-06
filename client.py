import asyncio

import logging

import grpc
import mafia_pb2
import mafia_pb2_grpc

import random
import sys

async def run():
    #name can be set in command line arguments or manually later
    mode = 'manual'
    user_input = ''
    if len(sys.argv) > 1:
        mode = 'auto'
        user_input = str(sys.argv[1])
    if mode == 'manual':
        print("Enter your name:")
        user_input = input()
    session = -1
    role = ''
    players = []
    guessed = False
    #when testing without Docker, use 'localhost:50051' instead of 'server:50051'
    async with grpc.aio.insecure_channel('server:50051') as channel:
        stub = mafia_pb2_grpc.MafiaStub(channel)
        #join the server and get the session number
        response = await stub.SayHello(mafia_pb2.HelloRequest(name=user_input))
        if mode == 'manual':
            while response.message[:4] == "Name":
                print(response.message)
                user_input = input()
                response = await stub.SayHello(mafia_pb2.HelloRequest(name=user_input))
        session = response.session
        print(response.message)
        #subscribe to update messages
        async for update in stub.SendUpdates(mafia_pb2.UpdateRequest(session=session,name=user_input)):
            print(update.message)
            message_array = update.message.split()
            if role == 'ghost':
                continue
            if len(message_array) > 1:
                #message that sets the role
                if message_array[1] == 'you':
                    role = message_array[-1]
                
                #message that notifies about new users
                elif message_array[1] == 'joined':
                    players.append(message_array[0])
                
                #message that notifies about new day
                elif message_array[0] == 'Day':
                    if role == 'commissioner' and guessed == True:
                        if random.randint(0, 1) == 1:
                            print("Chose to disclose mafia")
                            stub.RevealPlayer(mafia_pb2.UpdateRequest(session=session,name=user_input))
                        else:
                            print("Chose not to disclose mafia")
                    if random.randint(0, 1) == 1:
                        print("Chose to end day")
                        stub.EndDay(mafia_pb2.UpdateRequest(session=session,name=user_input))
                    chosen = random.randint(0, 3)
                    print("Chose to execute", players[chosen])
                    stub.ExecutePlayer(mafia_pb2.KillRequest(session=session,sender=user_input, \
                                                             victim=chosen))
                    guessed = False
                
                #message that notifies about new day
                elif message_array[0] == 'Night':
                    if role == 'commissioner':
                        chosen = random.randint(0, 3)
                        print("Chose to check", players[chosen])
                        response = await stub.CheckPlayer(mafia_pb2.KillRequest(session=session, \
                                                                                sender=user_input, \
                                                                                victim=chosen))
                        if response.message == 'Correct':
                            print("Was right", players[chosen], "is mafia")
                            guessed = True
                        else:
                            print("Was wrong", players[chosen], "is not mafia")
                    elif role == 'mafia':
                        chosen = random.randint(0, 3)
                        print("Chose to kill", players[chosen])
                        stub.KillPlayer(mafia_pb2.KillRequest(session=session, sender=user_input, \
                                                                                victim=chosen))



if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())