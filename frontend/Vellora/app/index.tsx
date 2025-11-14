import { View, Text, Pressable, SafeAreaView } from "react-native";
import { router } from "expo-router";

export default function Index() {
  return (
    <SafeAreaView
      style={{
        flex: 1,
        backgroundColor: "#fff",
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
      }}
    >
      <Pressable
        onPress={() => router.push("/login")}
        style={{
          width: "100%",
          paddingVertical: 16,
          backgroundColor: "#3F46D6",
          borderRadius: 12,
          marginBottom: 20,
        }}
      >
        <Text
          style={{
            color: "#fff",
            textAlign: "center",
            fontSize: 18,
            fontWeight: "600",
          }}
        >
          Go to Login Page
        </Text>
      </Pressable>

      <Pressable
        onPress={() => router.push("/reimbursement")}
        style={{
          width: "100%",
          paddingVertical: 16,
          backgroundColor: "#22C55E",
          borderRadius: 12,
        }}
      >
        <Text
          style={{
            color: "#fff",
            textAlign: "center",
            fontSize: 18,
            fontWeight: "600",
          }}
        >
          Go to Reimbursement
        </Text>
      </Pressable>
    </SafeAreaView>
  );
}
