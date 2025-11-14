import ReimbursementRateListPage from "./components/ReimbursementRateListPage";
import { router } from "expo-router";
import LoginPage from "./pages/LoginPage";

export default function Index() {
	return (
		//<LoginPage />
		<ReimbursementRateListPage
			onCreateCustom={() => router.push("/reimbursement/add")}
			onOpenIRS={() => router.push("/reimbursement/irs")}
			onOpenCustomRate={(id) => router.push(`/reimbursement/${id}`)}
		/>
	);
}
