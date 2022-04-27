import heap2

def main(){

    slate = []
    ##### TODO: implement game data finder 
    ##### user date input if not here
    for n, game in enumerate(slate):
        #### get data

        temp = basic_info(### home team, ### away team, ### Point Differential)

        insert(slate, temp)

    print("The closest game on {date} is the {slate[0].away} at {slate[0].home}")
    print("The predicted point differential is {slate[0].PD}")

}