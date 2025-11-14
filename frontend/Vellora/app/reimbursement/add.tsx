import { router } from "expo-router";
import AddCustomRatePage from "../components/AddCustomRatePage";

export default function Page() {
  return (
    <AddCustomRatePage
      onClose={() => router.back()}
      onSave={() => router.back()}
    />
  );
}
