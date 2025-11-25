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
  const [userBackground, setUserBackground] = useState("");

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
    <div className="flex min-h-svh flex-row items-start justify-center gap-8 p-8">
      {/* Left: Catalog */}
      <div className="flex-1">
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
      {/* Right: Recommendation Panel */}
      <div className="w-full max-w-sm bg-white rounded-lg shadow-md p-6 flex flex-col gap-4">
        <label htmlFor="user-background" className="font-medium text-lg mb-2">
          Please describe your background:
        </label>
        <textarea
          id="user-background"
          className="border rounded-md p-2 min-h-[120px] resize-none"
          value={userBackground}
          onChange={(e) => setUserBackground(e.target.value)}
          placeholder="E.g. dietary preferences, allergies, etc."
        />
        <Button className="self-end" variant="default">
          Recommend
        </Button>
      </div>
    </div>
  );
}

export default App;
