import { useLocalSearchParams } from "expo-router";
import ReimbursementRateListPage from "../components/ReimbursementRateListPage";
import { router } from "expo-router";
import { useState } from "react";

export default function Index() {
  const params = useLocalSearchParams();
  const [customRates, setCustomRates] = useState<any[]>([]);

  if (params.newRate) {
    try {
      const parsed = JSON.parse(String(params.newRate));
      if (!customRates.find((r) => r.id === parsed.id)) {
        setCustomRates((prev) => [...prev, parsed]);
      }
    } catch (e) {}
  }

  return (
    <ReimbursementRateListPage
      rates={customRates}
      onCreateCustom={() => router.push("/reimbursement/add")}
      onOpenIRS={() => router.push("/reimbursement/irs")}
      onOpenCustomRate={(id) => {
        const found = customRates.find((r) => r.id === id);
        if (found) {
          router.push({
            pathname: "/reimbursement/details",
            params: { data: JSON.stringify(found) },
          });
        }
      }}
    />
  );
}
