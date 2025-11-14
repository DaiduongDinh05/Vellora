import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Linking,
  Image,
} from "react-native";
import { styles } from "../styles/LoginStyles";
import { getProviderAuthorizeUrl, login } from "../services/auth";
import { router } from "expo-router";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await login(email.trim(), password);

      setMessage(
        `Welcome ${
          response.user.full_name ?? response.user.email
        }! Access token expires in ${Math.round(
          response.tokens.access_token_expires_in / 60
        )} minutes.`
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getProviderAuthorizeUrl("google");
      await Linking.openURL(data.authorization_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.safe}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      keyboardVerticalOffset={50}
    >
      <View style={styles.container}>
        <View style={styles.logoRow}>
          <Image
            source={require("../assets/Vellora_Dark_Logo.png")}
            style={styles.logoImage}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Email"
            placeholderTextColor="#9CA3AF"
            autoCapitalize="none"
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Password"
            placeholderTextColor="#9CA3AF"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />
        </View>

        {error && <Text style={[styles.message, styles.messageError]}>{error}</Text>}
        {message && (
          <Text style={[styles.message, styles.messageSuccess]}>{message}</Text>
        )}

        <View style={{ width: "100%", alignItems: "center", marginTop: 16 }}>
          <Pressable
            disabled={loading}
            onPress={handleSubmit}
            style={({ pressed }) => [
              styles.secondaryButton,
              pressed && { opacity: 0.85 },
              loading && { opacity: 0.6 },
              { width: "100%" },
            ]}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.ctaText}>Login</Text>
            )}
          </Pressable>
        </View>

        <View style={{ width: "100%", alignItems: "center", marginTop: 16 }}>
          <Pressable
            disabled={loading}
            onPress={handleGoogleSignIn}
            style={({ pressed }) => [
              styles.secondaryButton,
              pressed && { opacity: 0.85 },
              loading && { opacity: 0.6 },
              { width: "100%" },
            ]}
          >
            <Text style={styles.secondaryButtonText}>Continue with Google</Text>
          </Pressable>
        </View>

        <Text style={styles.footerText}>
          Don't have an account?{" "}
          <Text
            style={styles.link}
            onPress={() => router.push("/pages/Register")}
          >
            Sign up
          </Text>
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}
