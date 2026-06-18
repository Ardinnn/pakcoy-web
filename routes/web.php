<?php

use App\Http\Controllers\PakcoyController;
use Illuminate\Support\Facades\Route;

// 1. Rute Utama untuk menampilkan halaman dashboard PakcoyAI beserta data riwayatnya
Route::get('/', [PakcoyController::class, 'index'])->name('dashboard');

// 2. Rute API/AJAX untuk menyimpan riwayat hasil prediksi dari JavaScript ke MySQL
Route::post('/simpan-riwayat', [PakcoyController::class, 'simpanRiwayat'])->name('riwayat.simpan');