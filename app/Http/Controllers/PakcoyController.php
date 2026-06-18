<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PakcoyController extends Controller
{
    // Tampilkan halaman utama dengan menyertakan data riwayat dari MySQL
    public function index()
    {
        $riwayat = DB::table('pakcoy_histories')->latest()->take(10)->get();
        return view('dashboard', compact('riwayat'));
    }

    // Fungsi khusus menerima setoran data hasil AI dari JavaScript untuk disimpan ke MySQL
    public function simpanRiwayat(Request $request)
    {
        $request->validate([
            'jenis_fitur' => 'required|string',
            'hasil_prediksi' => 'required|string',
            'tingkat_akurasi' => 'nullable|numeric',
        ]);

        DB::table('pakcoy_histories')->insert([
            'jenis_fitur' => $request->jenis_fitur,
            'file_gambar' => $request->file_gambar ?? null, // Opsional jika ingin mencatat nama file
            'hasil_prediksi' => $request->hasil_prediksi,
            'tingkat_akurasi' => $request->tingkat_akurasi,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        return response()->json(['status' => 'success', 'message' => 'Log berhasil disimpan ke MySQL']);
    }
}