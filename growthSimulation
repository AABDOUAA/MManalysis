# Function to initialize the network
def my_initialize_network(final_uni_network, popDictionary, probDictionary):
    # Initialize university populations and connections
    universities = {}

    for uni in popDictionary.keys():
      pops = popDictionary[uni]
      prob = probDictionary[uni]
      universities[uni] = {'staff': pops[0], 'students': pops[1], 'staff_users': 0, 'student_users': 0, 'prob_trans': prob, 'student_trigger': 0, 'trigger_time': 0}

    # Initialize the number of initial users for University A
    universities['university college london']['staff_users'] = 5

    # Create the network graph
    G = nx.Graph()

    # Add edges to the graph from the network dictionary
    for node, connections in final_uni_network.items():
        for connected_node in connections:
            G.add_edge(node, connected_node)

    return G, universities

def plot_user_growth_time(user_numbers, total_numbers, user_type, num_timesteps, start_date):
    # Calculate the list of dates
    dates = [start_date + datetime.timedelta(days=30*i) for i in range(num_timesteps)]

    # Plot user growth
    for uni, numbers in user_numbers.items():
        plt.plot(dates, numbers, label=uni)
    # plt.plot(dates, total_numbers, label='Total')

    # Set plot labels and title
    plt.xlabel('Year')
    plt.ylabel('Number of ' + user_type + ' Users')
    plt.title(user_type + ' User Growth Over Time')

    # Customize x-axis ticks
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability


    # Ensure plot layout is tight
    plt.tight_layout()

    # Show the plot
    plt.show()

# CURRENT STATE:
# have this basic propogation and user tracking function!
# to note: timesteps need to be dealt with more realistically
# currently way too much activity from step to step
# also need to include timing for network propogation
# at the moment at every timestep there is a positive increase in
# users - however in reality this must be more random and non-guaranteed
# the growth of staff numbers is also initiated randomly and is not influenced
# at all by the connectivity of the network


# Function to update user numbers in universities
def update_user_numbers(G, universities, growth_params, timestep):

    start_date = datetime.datetime(2024, 5, 29)
    timestep_interval = datetime.timedelta(days=30)
    current_date = start_date + timestep_interval * timestep

    for uni, data in universities.items():
        max_staff_users = growth_params['max_staff_users'] * data['staff']
        max_student_users = growth_params['max_student_users'] * data['students']
        if timestep == 0:
          staff_growth = 0
          universities[uni]['staff_users'] += staff_growth
        else:

          if data['staff_users'] == 0:
            # starting conditions for initiating growth - need to check that it is connected to someone with users]
            # check to see if neighbours have users
            for neighbor in G.neighbors(uni):
              neighbor_data = universities[neighbor]
              if neighbor_data['staff_users'] == 0:
                staff_growth = 0
              else:
                random_number = np.random.rand()
                if random_number < data['prob_trans']:
                  staff_growth = 1 # this is beginning of 1 now and then increasing to 5 after 6 months
                  universities[uni]['staff_users'] += staff_growth
                else:
                  staff_growth = 0

          else: # this controls normal growth within the university (where here it is just random)
                    # but could be extended to be increased by neighbours too - eg someone collabs in (although v small impact)
              if data['staff_users'] < max_staff_users:
                  staff_growth = np.random.binomial(max_staff_users - data['staff_users'], growth_params['staff_growth_rate'])
                  #staff_growth = np.ceil(np.random.normal(growth_params['staff_growth_rate'], 0.1))
                  universities[uni]['staff_users'] += staff_growth
        
              if data['student_users'] < max_student_users:
                if universities[uni]['trigger_time'] == 0:
                  if data['staff_users'] / max_staff_users >= growth_params['student_threshold']:
                    universities[uni]['student_trigger'] = 1
                    universities[uni]['trigger_time'] = timestep
                elif current_date.month == 9:
                  universities[uni]['student_users'] += 0.25 * max_student_users


                  # but the top-line condition that student users is less than
                  # max it will never go over the total possible


                  

            # this is the part that modulates the student onboarding - as can be seen the conditions for it are relatively simple
            # the first condition will always be true - until max students are reached
            # but second condition only becomes true after the threshold is met and stays true

# Function to simulate user growth over time
def simulate_growth(G, universities, growth_params, num_steps):
    staff_user_numbers = {uni: [] for uni in universities}
    student_user_numbers = {uni: [] for uni in universities}
    total_user_numbers = {uni: [] for uni in universities}

    total_staff_user = []
    total_student_user = []
    total_total_user = []

    for timestep in range(num_steps):  # Start from timestep 1
        update_user_numbers(G, universities, growth_params, timestep)
        # this is the method itself that increaces the numbers and it overrides
        # the attribute in the universities dictionary
        total_staff = 0
        total_student = 0
        total_total = 0
        for uni, data in universities.items():
            staff_user_numbers[uni].append(data['staff_users'])
            student_user_numbers[uni].append(data['student_users'])
            total_user_numbers[uni].append(data['staff_users'] + data['student_users'])
            # these are dictionaries that contain the time-series of the growth
            total_staff += data['staff_users']
            total_student += data['student_users']
            total_total = total_staff + total_student
        total_staff_user.append(total_staff)
        total_student_user.append(total_student)
        total_total_user.append(total_total)
    return staff_user_numbers, student_user_numbers, total_user_numbers, total_staff_user, total_student_user, total_total_user

# Function to plot user numbers over time
def plot_user_growth(user_numbers, total_numbers, user_type):
    for uni, numbers in user_numbers.items():
        plt.plot(numbers, label=uni)
    plt.plot(total_numbers, label = 'Total')
    plt.xlabel('Time')
    plt.ylabel('Number of ' + user_type + ' Users')
    # plt.legend()
    plt.title(user_type + ' User Growth Over Time')
    plt.show()
