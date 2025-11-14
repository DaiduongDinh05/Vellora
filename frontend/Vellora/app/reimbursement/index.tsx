import { useState, useEffect } from "react";
import { useLocalSearchParams, router } from "expo-router";
import ReimbursementRateListPage from "../components/ReimbursementRateListPage";

type Category = { id: string; name: string; rate: string };

type CustomRate = {
  id: string;
  name: string;
  description: string;
  year: string;
  categories: Category[];
};

export default function Index() {
  const params = useLocalSearchParams();
  const [customRates, setCustomRates] = useState<CustomRate[]>([]);

  useEffect(() => {
    if (params.newRate && typeof params.newRate === "string") {
      try {
        const parsed: CustomRate = JSON.parse(params.newRate);
        setCustomRates((prev) => {
          if (prev.some((r) => r.id === parsed.id)) return prev;
          return [...prev, parsed];
        });
      } catch {}
    }
  }, [params.newRate]);

  return (
    <ReimbursementRateListPage
      rates={customRates}
      onCreateCustom={() => router.push("/reimbursement/add")}
      onOpenIRS={() => router.push("/reimbursement/irs")}
      onOpenCustomRate={(id) =>
        router.push({
          pathname: "/reimbursement/details",
          params: { id },
        })
      }
    />
  );
}
