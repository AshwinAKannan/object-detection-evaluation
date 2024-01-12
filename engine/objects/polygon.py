class Polygon:
    # Image Space Polygon
    def __init__(self, points: tuple) -> None:
        self.vertices: tuple = points
        self.num_vertices: int = len(self.vertices)

        # image space -> ensure (x, y) is always >= 0
        for vertex in self.vertices:
            assert vertex[0] >= 0 and vertex[1] >= 0,\
                f"Image Space Polygon expects vertex (x, y) to be >=0. Found ({vertex[0]}, {vertex[1]})"

    def area(self) -> float:
        # Shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula
        if self.num_vertices < 3:
            return 0.0
        
        # area will be negative for clockwise polygon vertices,
        # postive for counter-clockwise vertices
        area = 0.0
        for i in range(self.num_vertices):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % self.num_vertices]
            
            # calculate determinant and add
            area += (x1 * y2 - x2 * y1)
        
        return abs(area) / 2.0
        
        