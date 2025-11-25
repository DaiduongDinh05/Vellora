import { Text, View } from "react-native";
import { Link } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { getProviderAuthorizeUrl, login } from "../services/auth";
// import Tracking from "../components/tracking";

export default function Index() {
  
  return (
    <SafeAreaView className="flex-1 justify-start p-[25px]"
    >
      <Text className="text-5xl text-primaryPurple font-bold">Welcome back,</Text>
      <Link href="../tracking">Live track a trip</Link>
      <Link href="../manualLogScreen">Manually log a trip</Link>
      <Link href="../trackingTest"></Link>
      {/* <Tracking></Tracking> */}
    </SafeAreaView>
  );
}
