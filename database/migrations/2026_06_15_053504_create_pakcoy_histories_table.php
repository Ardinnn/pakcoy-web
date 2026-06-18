<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('pakcoy_histories', function (Blueprint $table) {
            $table->id();
            $table->string('jenis_fitur'); // 'CNN' (Gambar) atau 'LSTM' (Sensor)
            $table->string('file_gambar')->nullable(); // Menyimpan nama file foto pakcoy
            $table->string('hasil_prediksi'); // 'siap-panen', atau angka prediksi kelembapan (misal: '78.5%')
            $table->float('tingkat_akurasi')->nullable(); // Khusus CNN (misal: 95.5)
            $table->timestamps(); // Otomatis membuat kolom created_at (waktu deteksi)
            
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('pakcoy_histories');
    }
};
