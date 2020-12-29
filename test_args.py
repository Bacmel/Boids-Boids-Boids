from src.arguments import getArgs

if __name__ == "__main__":
    args = getArgs()
    print("n= ",args.n)
    print("fps= ",args.fps)
    print("res= ", args.res)
    print("highlight= ", args.highlight)
    print("preview only= ", args.preview_only)
    print("render= ", args.render)
    print("verbose= ", args.verbose)

    print()

    print("attraction= ",args.attraction_radius)
    print('orientation= ', args.orientation_radius)
    print("repulsion= ", args.repulsion_radius)

    print()

    print("border= ", args.border)
    
    print()

    print("knn= ", args.num_neighbors)
    print("diff threshold= ", args.diff_threshold)
    print("view distance= ", args.view_dist)
    print("blindspot direction= ", args.blindspot_direction)
    print("blindspot opening= ", args.blindspot_opening)

    #if args.blindspot_direction == None or args.blindspot_opening == None and len(args.blindspot_direction) != len(args.blindspot_opening):
    #    print("***ERROR: wrong arguments: length of blindspot direction different than the length of blindspot opening")
    #    exit()
    
    if args.blindspot_direction == None and args.blindspot_opening == None:
        print("***WARNING: in arguments: no blindspot specified")
    elif not(args.blindspot_direction and args.blindspot_opening):
        print("***ERROR: wrong arguments: miss either blindspot direction or blingspot opening")
        exit()
    elif len(args.blindspot_direction) != len(args.blindspot_opening):
        print("***ERROR: wrong arguments: length of blindspot direction different than length of blindspot opening")
        exit()
    
    print()

    print("turning rate= ", args.turning_rate)
    print("boid velocity= ", args.boid_speed)
    print("error= ", args.error_params)

    if ":" not in args.error_params:
        print("***ERROR: wrong argument: in '--error', must be 'mu;std'")
        exit()