import { router } from "expo-router";
import ViewIRSRatePage from "../components/ViewIRSRatePage";

export default function Page() {
  return <ViewIRSRatePage onBack={() => router.back()} />;
}
