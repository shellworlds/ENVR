#!/bin/bash
# Shell: Client Encryption Automation Framework
# Automated encryption processes for client data protection

set -euo pipefail

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONFIG_DIR="./encryption_configs"
KEY_STORE="./keys"
AUDIT_LOG="./audit/encryption_audit.log"
BACKUP_DIR="./backups"
COMPLIANCE_REPORTS="./reports"

# Initialize directories
init_directories() {
    echo -e "${BLUE}Initializing encryption directories...${NC}"
    mkdir -p "$CONFIG_DIR" "$KEY_STORE" "$BACKUP_DIR" "$COMPLIANCE_REPORTS" "./audit"
    touch "$AUDIT_LOG"
    echo "✅ Directories initialized"
}

# Log function for audit trail
log_audit() {
    local action=$1
    local client_id=$2
    local details=$3
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "$timestamp | CLIENT:$client_id | ACTION:$action | DETAILS:$details" >> "$AUDIT_LOG"
    echo -e "${GREEN}[AUDIT] $action for $client_id${NC}"
}

# Generate encryption keys for client
generate_client_keys() {
    local client_id=$1
    local encryption_type=$2
    
    echo -e "${BLUE}Generating keys for $client_id ($encryption_type)...${NC}"
    
    case $encryption_type in
        "aes-256-gcm")
            # Generate AES-256 key
            openssl rand -base64 32 > "$KEY_STORE/${client_id}_aes.key"
            log_audit "key_generation" "$client_id" "aes-256-gcm key created"
            ;;
        "rsa-4096")
            # Generate RSA key pair
            openssl genrsa -out "$KEY_STORE/${client_id}_rsa_private.pem" 4096
            openssl rsa -in "$KEY_STORE/${client_id}_rsa_private.pem" -pubout \
                -out "$KEY_STORE/${client_id}_rsa_public.pem"
            log_audit "key_generation" "$client_id" "rsa-4096 keypair created"
            ;;
        "chacha20")
            # Generate ChaCha20 key
            openssl rand -base64 32 > "$KEY_STORE/${client_id}_chacha.key"
            log_audit "key_generation" "$client_id" "chacha20-poly1305 key created"
            ;;
        *)
            echo -e "${RED}Unknown encryption type: $encryption_type${NC}"
            return 1
            ;;
    esac
    
    # Secure key permissions
    chmod 600 "$KEY_STORE/${client_id}"*
    echo "✅ Keys generated and secured"
}

# Encrypt file for client
encrypt_file() {
    local client_id=$1
    local input_file=$2
    local output_file="${input_file}.enc"
    
    echo -e "${BLUE}Encrypting $input_file for $client_id...${NC}"
    
    # Check for existing keys
    if [[ -f "$KEY_STORE/${client_id}_aes.key" ]]; then
        local key_file="$KEY_STORE/${client_id}_aes.key"
        local algorithm="aes-256-gcm"
        
        # Encrypt with AES-GCM
        openssl enc -aes-256-gcm \
            -in "$input_file" \
            -out "$output_file" \
            -pass file:"$key_file" \
            -pbkdf2
        
    elif [[ -f "$KEY_STORE/${client_id}_rsa_public.pem" ]]; then
        # Generate session key for RSA encryption
        local session_key=$(openssl rand -base64 32)
        local encrypted_key="${output_file}.key.enc"
        
        # Encrypt session key with RSA
        echo "$session_key" | openssl pkeyutl -encrypt \
            -pubin -inkey "$KEY_STORE/${client_id}_rsa_public.pem" \
            -out "$encrypted_key"
        
        # Encrypt data with session key
        openssl enc -aes-256-cbc \
            -in "$input_file" \
            -out "$output_file" \
            -k "$session_key" \
            -pbkdf2
        
        algorithm="rsa-aes-hybrid"
        
    else
        echo -e "${RED}No keys found for $client_id${NC}"
        return 1
    fi
    
    log_audit "file_encryption" "$client_id" "$input_file -> $output_file ($algorithm)"
    echo "✅ File encrypted: $output_file"
}

# Decrypt file for client
decrypt_file() {
    local client_id=$1
    local input_file=$2
    local output_file="${input_file%.enc}"
    
    echo -e "${BLUE}Decrypting $input_file for $client_id...${NC}"
    
    if [[ -f "$KEY_STORE/${client_id}_aes.key" ]]; then
        openssl enc -aes-256-gcm -d \
            -in "$input_file" \
            -out "$output_file" \
            -pass file:"$KEY_STORE/${client_id}_aes.key" \
            -pbkdf2
            
    elif [[ -f "$KEY_STORE/${client_id}_rsa_private.pem" && -f "${input_file}.key.enc" ]]; then
        # Decrypt session key
        local session_key=$(openssl pkeyutl -decrypt \
            -inkey "$KEY_STORE/${client_id}_rsa_private.pem" \
            -in "${input_file}.key.enc")
        
        # Decrypt data with session key
        openssl enc -aes-256-cbc -d \
            -in "$input_file" \
            -out "$output_file" \
            -k "$session_key" \
            -pbkdf2
            
    else
        echo -e "${RED}Cannot decrypt: missing keys${NC}"
        return 1
    fi
    
    log_audit "file_decryption" "$client_id" "$input_file -> $output_file"
    echo "✅ File decrypted: $output_file"
}

# Key rotation process
rotate_keys() {
    local client_id=$1
    
    echo -e "${YELLOW}Rotating keys for $client_id...${NC}"
    
    # Backup old keys
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    mkdir -p "$BACKUP_DIR/$client_id"
    
    if [[ -f "$KEY_STORE/${client_id}_aes.key" ]]; then
        cp "$KEY_STORE/${client_id}_aes.key" \
           "$BACKUP_DIR/$client_id/aes.key.$backup_timestamp"
        
        # Generate new key
        generate_client_keys "$client_id" "aes-256-gcm"
        
    elif [[ -f "$KEY_STORE/${client_id}_rsa_private.pem" ]]; then
        cp "$KEY_STORE/${client_id}_rsa_private.pem" \
           "$BACKUP_DIR/$client_id/rsa_private.pem.$backup_timestamp"
        cp "$KEY_STORE/${client_id}_rsa_public.pem" \
           "$BACKUP_DIR/$client_id/rsa_public.pem.$backup_timestamp"
        
        # Generate new key pair
        generate_client_keys "$client_id" "rsa-4096"
    fi
    
    log_audit "key_rotation" "$client_id" "keys rotated and backed up"
    echo "✅ Keys rotated successfully"
}

# Generate compliance report
generate_compliance_report() {
    local client_id=$1
    
    echo -e "${BLUE}Generating compliance report for $client_id...${NC}"
    
    local report_file="$COMPLIANCE_REPORTS/${client_id}_$(date +%Y%m%d).md"
    
    cat > "$report_file" << REPORT
# Encryption Compliance Report
## Client: $client_id
## Date: $(date)

## Key Inventory
$(ls -la "$KEY_STORE/${client_id}"* 2>/dev/null | awk '{print " - " $9 " (" $5 " bytes)"}')

## Audit Trail (Last 10 entries)
$(tail -10 "$AUDIT_LOG" | grep "CLIENT:$client_id" | sed 's/^/ - /')

## Security Status
- Key Rotation: $(find "$KEY_STORE" -name "${client_id}*" -mtime -30 | head -1 | \
    xargs -I {} test {} && echo "✅ Within 30 days" || echo "⚠️  Needs rotation")
- Audit Logging: ✅ Enabled
- Backup Status: $(ls "$BACKUP_DIR/$client_id" 2>/dev/null | head -1 | \
    xargs -I {} test {} && echo "✅ Backups exist" || echo "⚠️  No backups")

## Recommendations
1. Review key rotation schedule
2. Verify backup integrity
3. Update compliance documentation

---
*Report generated automatically by Encryption Automation Framework*
REPORT
    
    log_audit "report_generation" "$client_id" "compliance report created"
    echo "✅ Report generated: $report_file"
}

# Health check function
health_check() {
    echo -e "${BLUE}Running encryption system health check...${NC}"
    
    local errors=0
    
    # Check directories
    for dir in "$CONFIG_DIR" "$KEY_STORE" "$BACKUP_DIR" "$COMPLIANCE_REPORTS"; do
        if [[ -d "$dir" ]]; then
            echo "✅ $dir exists"
        else
            echo -e "${RED}✗ $dir missing${NC}"
            ((errors++))
        fi
    done
    
    # Check audit log
    if [[ -f "$AUDIT_LOG" ]]; then
        echo "✅ Audit log exists ($(wc -l < "$AUDIT_LOG") entries)"
    else
        echo -e "${RED}✗ Audit log missing${NC}"
        ((errors++))
    done
    
    # Check OpenSSL availability
    if command -v openssl &> /dev/null; then
        echo "✅ OpenSSL available ($(openssl version))"
    else
        echo -e "${RED}✗ OpenSSL not found${NC}"
        ((errors++))
    done
    
    if [[ $errors -eq 0 ]]; then
        echo -e "${GREEN}✅ All health checks passed${NC}"
    else
        echo -e "${RED}⚠️  Found $errors issues${NC}"
    fi
    
    return $errors
}

# Main menu
main_menu() {
    echo -e "\n${BLUE}=================================${NC}"
    echo -e "${BLUE}   Client Encryption Framework   ${NC}"
    echo -e "${BLUE}=================================${NC}"
    
    while true; do
        echo -e "\nOptions:"
        echo "1) Initialize system"
        echo "2) Generate client keys"
        echo "3) Encrypt file"
        echo "4) Decrypt file"
        echo "5) Rotate keys"
        echo "6) Generate compliance report"
        echo "7) System health check"
        echo "8) View audit log"
        echo "9) Exit"
        
        read -p "Select option: " choice
        
        case $choice in
            1) init_directories ;;
            2) 
                read -p "Client ID: " client_id
                read -p "Encryption type (aes-256-gcm/rsa-4096/chacha20): " enc_type
                generate_client_keys "$client_id" "$enc_type"
                ;;
            3)
                read -p "Client ID: " client_id
                read -p "File to encrypt: " input_file
                encrypt_file "$client_id" "$input_file"
                ;;
            4)
                read -p "Client ID: " client_id
                read -p "File to decrypt: " input_file
                decrypt_file "$client_id" "$input_file"
                ;;
            5)
                read -p "Client ID: " client_id
                rotate_keys "$client_id"
                ;;
            6)
                read -p "Client ID: " client_id
                generate_compliance_report "$client_id"
                ;;
            7) health_check ;;
            8) less "$AUDIT_LOG" ;;
            9) 
                echo -e "${GREEN}Exiting...${NC}"
                exit 0
                ;;
            *) echo -e "${RED}Invalid option${NC}" ;;
        esac
    done
}

# Run main menu if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_menu
fi

