import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useEffect, useState } from "react";
import { getCatalog } from "./api";

function App() {
  const [catalog, setCatalog] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCatalog().then((data) => {
      setCatalog(data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-svh flex-col items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {catalog.map((item) => (
          <Card key={item.id} className="w-[320px]">
            <CardHeader>
              <img
                src={item.image_url}
                alt={item.name}
                className="rounded-md w-full h-40 object-cover mb-2"
              />
              <CardTitle>{item.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{item.description}</p>
              <p className="mt-2 text-sm text-muted-foreground">
                Calories: {item.calories} |{" "}
                {item.is_vegan ? "Vegan" : "Non-Vegan"}
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline">Details</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default App;
