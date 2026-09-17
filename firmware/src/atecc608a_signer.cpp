#include <Arduino.h>
#include <Wire.h>
#include "mbedtls/sha256.h"

#define I2C_SDA 8
#define I2C_SCL 9
#define ATECC608A_ADDR 0x60
#define PRIVATE_KEY_SLOT 0

struct AttestedPacket {
uint32_t monotonic_counter;
uint64_t timestamp_epoch_ms;
char fhir_observation_hash[65];
uint8_t signature_r[32];
uint8_t signature_s[32];
};

bool sign_vitals_payload(const char* payload_json, AttestedPacket* out_packet, uint32_t counter) {
uint8_t hash[32];
mbedtls_sha256_context ctx;
mbedtls_sha256_init(&ctx);
mbedtls_sha256_starts(&ctx, 0);
mbedtls_sha256_update(&ctx, (const unsigned char*)payload_json, strlen(payload_json));
mbedtls_sha256_finish(&ctx, hash);
mbedtls_sha256_free(&ctx);

for (int i = 0; i < 32; i++) {
    sprintf(&out_packet->fhir_observation_hash[i * 2], "%02x", hash[i]);
}
out_packet->monotonic_counter = counter;
out_packet->timestamp_epoch_ms = millis();

Wire.beginTransmission(ATECC608A_ADDR);
Wire.write(0x41);
Wire.write(PRIVATE_KEY_SLOT);
Wire.write(hash, 32);
uint8_t status = Wire.endTransmission();

return (status == 0);
}
