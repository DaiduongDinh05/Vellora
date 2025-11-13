// login.tsx – UI-only screen
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
} from "react-native";
import { styles } from "../styles/LoginStyles";
import { getProviderAuthorizeUrl, login, register } from "../services/auth";

type AuthMode = "login" | "register";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<AuthMode>("login");
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
      const response =
        mode === "login"
          ? await login(email.trim(), password)
          : await register({ email: email.trim(), password });

      setMessage(
        `Welcome ${response.user.full_name ?? response.user.email}! Access token expires in ${Math.round(
          response.tokens.access_token_expires_in / 60,
        )} minutes.`,
      );
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong, please try again.",
      );
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
      setError(
        err instanceof Error ? err.message : "Unable to start Google sign-in right now.",
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode((prev) => (prev === "login" ? "register" : "login"));
    setError(null);
    setMessage(null);
  };

  return (
    <KeyboardAvoidingView
      style={styles.safe}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.container}>
        <View style={styles.logoRow}>
          <Text style={styles.logoText}>Vell</Text>
          <View style={styles.logoMark}>
            <View style={styles.logoMarkInner} />
          </View>
          <Text style={styles.logoText}>ra</Text>
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Email Here"
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

        {error ? (
          <Text style={[styles.message, styles.messageError]}>{error}</Text>
        ) : null}
        {message ? (
          <Text style={[styles.message, styles.messageSuccess]}>{message}</Text>
        ) : null}

        <Pressable
          disabled={loading}
          onPress={handleSubmit}
          style={({ pressed }) => [
            styles.cta,
            pressed && { opacity: 0.9 },
            loading && { opacity: 0.6 },
          ]}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.ctaText}>
              {mode === "login" ? "Sign in" : "Create account"}
            </Text>
          )}
        </Pressable>

        <Pressable
          disabled={loading}
          onPress={handleGoogleSignIn}
          style={({ pressed }) => [
            styles.secondaryButton,
            pressed && { opacity: 0.85 },
            loading && { opacity: 0.6 },
          ]}
        >
          <Text style={styles.secondaryButtonText}>Continue with Google</Text>
        </Pressable>

        <Text style={styles.footerText}>
          {mode === "login" ? "Don't have an account? " : "Already have an account? "}
          <Text style={styles.link} onPress={toggleMode}>
            {mode === "login" ? "Sign up" : "Sign in"}
          </Text>
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}
