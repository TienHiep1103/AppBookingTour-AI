class ItemType():
    TOUR = 1
    ACCOMMODATION = 2
    COMBO = 3

class VehicleType():
    CAR = 1
    AIRPLANE = 2
    
    @staticmethod
    def get_name(vehicle_type: int) -> str:
        if vehicle_type == VehicleType.CAR:
            return "Xe ô tô"
        elif vehicle_type == VehicleType.AIRPLANE:
            return "Máy bay"
        return "Không xác định"