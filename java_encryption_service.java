// Java: Client Encryption Service
// Enterprise-grade encryption implementation
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.util.Base64;
import java.security.SecureRandom;

public class EncryptionService {
    
    private static final String ALGORITHM = "AES/GCM/NoPadding";
    private static final int KEY_SIZE = 256;
    private static final int GCM_TAG_LENGTH = 128;
    
    public static class EncryptionResult {
        private String ciphertext;
        private String keyId;
        private String algorithm;
        
        // Getters and setters
        public String getCiphertext() { return ciphertext; }
        public void setCiphertext(String ciphertext) { this.ciphertext = ciphertext; }
        
        public String getKeyId() { return keyId; }
        public void setKeyId(String keyId) { this.keyId = keyId; }
        
        public String getAlgorithm() { return algorithm; }
        public void setAlgorithm(String algorithm) { this.algorithm = algorithm; }
    }
    
    public static EncryptionResult encrypt(String plaintext) throws Exception {
        // Generate AES key
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(KEY_SIZE);
        SecretKey secretKey = keyGen.generateKey();
        
        // Generate IV
        byte[] iv = new byte[12];
        SecureRandom random = new SecureRandom();
        random.nextBytes(iv);
        
        // Initialize cipher
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, spec);
        
        // Encrypt
        byte[] ciphertext = cipher.doFinal(plaintext.getBytes());
        
        // Prepare result
        EncryptionResult result = new EncryptionResult();
        result.setCiphertext(Base64.getEncoder().encodeToString(ciphertext));
        result.setAlgorithm("AES-256-GCM");
        result.setKeyId(generateKeyId());
        
        return result;
    }
    
    private static String generateKeyId() {
        return "key_" + System.currentTimeMillis() + "_" + 
               Integer.toHexString(new SecureRandom().nextInt());
    }
    
    public static void main(String[] args) {
        try {
            System.out.println("🚀 Java Encryption Service");
            EncryptionResult result = encrypt("Sensitive client data");
            System.out.println("Encryption successful!");
            System.out.println("Algorithm: " + result.getAlgorithm());
            System.out.println("Key ID: " + result.getKeyId());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
