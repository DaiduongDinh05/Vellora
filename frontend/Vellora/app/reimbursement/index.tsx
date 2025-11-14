import { router } from "expo-router";
import ReimbursementRateListPage from "../components/ReimbursementRateListPage";

export default function Page() {
  return (
    <ReimbursementRateListPage
      onCreateCustom={() => router.push("/reimbursement/add")}
      onOpenIRS={() => router.push("/reimbursement/irs")}
      onOpenCustomRate={(id) => router.push(`/reimbursement/${id}`)}
    />
  );
}
