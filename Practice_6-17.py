class Road:
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance


class Warehouse:
    def __init__(self, name, content=0):
        self.name = name
        self.content = content
        self.road_out = None
        self.queue_in = []
        self.queue_out = []

    def __str__(self):
        return 'Склад {} груза {}'.format(self.name, self.content)

    def set_road_out(self, road):
        self.road_out = road

    def truck_arrived(self, truck):
        self.queue_in.append(truck)
        truck.place = self.name
        print('{} приехал грузовик {} '.format(self.name, truck))

    def get_next_truck(self):
        if self.queue_in:
            truck = self.queue_in.pop()
            return truck

    def truck_ready(self, truck):
        self.queue_out.append(truck)
        print('{} грузовик готов {}'.format(self.name, truck))

    def act(self):
        while self.queue_out:
            truck = self.queue_out.pop()
            truck.go_to(road=self.road_out)


class Vehicle:
    fuel_rate = 0

    def __init__(self, model):
        self.model = model
        self.fuel = 0

    def __str__(self):
        return '{} топлива {} '.format(self.model, self.fuel)

    def tank_up(self):
        self.fuel += 1000
        # return '{} заправился'.format(self.model)
        print('{} заправился'.format(self.model))


class Truck(Vehicle):
    fuel_rate = 50

    def __init__(self, model, body_space=1000):
        super(Truck, self).__init__(model=model)
        self.body_space = body_space
        self.cargo = 0
        self.place = None
        self.velocity = 100
        self.distance_to_target = 0

    def __str__(self):
        res = super().__str__()
        return res + 'груза {}'.format(self.cargo)

    def ride(self):
        self.fuel -= self.fuel_rate
        if self.distance_to_target > self.velocity:
            self.distance_to_target -= self.velocity
            print('{} едет по дороге, осталось {}'.format(self.model, self.distance_to_target))
        else:
            self.place.end.truck_arrived(self)
            print('{} доехал'.format(self.model))

    def go_to(self, road):
        self.place = road
        self.distance_to_target = road.distance
        print('{} выехал в путь'.format(self.model))

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
        elif isinstance(self.place, Road):
            self.ride()


class AutoLoader(Vehicle):
    fuel_rate = 30

    def __init__(self, model, bucket_capacity=100, warehouse=None, role="loader"):
        super().__init__(model=model)
        self.truck_cargo_rest = None
        self.bucket_capacity = bucket_capacity
        self.warehouse = warehouse
        self.role = role
        self.truck = None

    def __str__(self):
        res = super().__str__()
        return res + 'грузим {}'.format(self.truck)

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
        elif self.truck is None:
            self.truck = self.warehouse.get_next_truck()
            print('{} взял в работу {}'.format(self.model, self.truck))
        elif self.role == 'loader':
            self.load()
        else:
            self.unload()

    def load(self):
        self.fuel -= self.fuel_rate
        truck_cargo_rest = self.truck.body_space - self.truck.cargo
        if truck_cargo_rest >= self.bucket_capacity:
            self.warehouse.content -= self.bucket_capacity
            self.truck.cargo += self.bucket_capacity
        else:
            self.warehouse.content -= self.truck_cargo_rest
            self.truck.cargo += self.truck_cargo_rest
        print('{} загрузил {}'.format(self.model, self.truck))
        if self.truck.cargo == self.truck.body_space:
            self.warehouse.truck_ready(self.truck)
            self.truck = None

    def unload(self):
        self.fuel -= self.fuel_rate
        if self.truck.cargo >= self.bucket_capacity:
            self.truck.cargo -= self.bucket_capacity
            self.warehouse.content += self.bucket_capacity
        else:
            self.truck.cargo -= self.truck.cargo
            self.warehouse.content += self.truck.cargo
        print('{} разгрузил {}'.format(self.model, self.truck))
        if self.truck.cargo == 0:
            self.warehouse.truck_ready(self.truck)
            self.truck = None


TOTAL_CARGO = 100000

moscow = Warehouse(name='Моска', content=TOTAL_CARGO)
piter = Warehouse(name='Санкт-Петербург', content=0)

moscow_piter = Road(start=moscow, end=piter, distance=715)
piter_moscow = Road(start=piter, end=moscow, distance=780)

moscow.set_road_out(moscow_piter)
piter.set_road_out(piter_moscow)

loader_1 = AutoLoader(model='Bobcat', bucket_capacity=1000, warehouse=moscow, role='loader')
loader_2 = AutoLoader(model='Lonking', bucket_capacity=500, warehouse=piter, role='unloader')

truck_1 = Truck(model='Камаз', body_space=5000)
truck_2 = Truck(model='Газ', body_space=2000)

moscow.truck_arrived(truck_1)
moscow.truck_arrived(truck_2)

hour = 0

while piter.content < TOTAL_CARGO:
    hour += 1
    print('------------------ Час {} ------------------'.format(hour))
    truck_1.act()
    truck_2.act()
    loader_1.act()
    loader_2.act()
    moscow.act()
    piter.act()
    print(truck_1)
    print(truck_2)
    print(loader_1)
    print(loader_2)
    print(moscow)
    print(piter)
