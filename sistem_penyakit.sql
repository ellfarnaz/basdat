-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Waktu pembuatan: 21 Des 2024 pada 01.16
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_penyakit`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `nama_admin` varchar(30) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` text DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id_admin`, `nama_admin`, `username`, `password`, `level`) VALUES
(1, 'Administrator', 'admin', 'admin123', 'super_admin');

-- --------------------------------------------------------

--
-- Struktur dari tabel `ciri_ciri`
--

CREATE TABLE `ciri_ciri` (
  `id_ciri_ciri` int(11) NOT NULL,
  `id_penyakit` int(11) DEFAULT NULL,
  `id_gejala` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `ciri_ciri`
--

INSERT INTO `ciri_ciri` (`id_ciri_ciri`, `id_penyakit`, `id_gejala`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 2, 1),
(5, 2, 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_penyebab`
--

CREATE TABLE `detail_penyebab` (
  `id_detail_penyebab` int(11) NOT NULL,
  `id_penyakit` int(11) DEFAULT NULL,
  `id_penyebab` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `detail_penyebab`
--

INSERT INTO `detail_penyebab` (`id_detail_penyebab`, `id_penyakit`, `id_penyebab`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `gejala`
--

CREATE TABLE `gejala` (
  `id_gejala` int(11) NOT NULL,
  `nama_gejala` text DEFAULT NULL,
  `id_admin` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `gejala`
--

INSERT INTO `gejala` (`id_gejala`, `nama_gejala`, `id_admin`) VALUES
(1, 'Demam Tinggi', 1),
(2, 'Sakit Kepala', 1),
(3, 'baba', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyakit`
--

CREATE TABLE `penyakit` (
  `id_penyakit` int(11) NOT NULL,
  `nama_penyakit` varchar(30) DEFAULT NULL,
  `images` varchar(200) DEFAULT NULL,
  `desk_penyakit` longtext DEFAULT NULL,
  `saran` longtext DEFAULT NULL,
  `id_admin` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `penyakit`
--

INSERT INTO `penyakit` (`id_penyakit`, `nama_penyakit`, `images`, `desk_penyakit`, `saran`, `id_admin`) VALUES
(1, 'Demam Berdarah', 'demam_berdarah.jpg', 'Penyakit yang disebabkan oleh virus dengue', 'Banyak minum air putih dan istirahat yang cukup', 1),
(2, 'baba', 'Easy_Indian_Chicken_and_Potato_Curry_-_Feast_with_Safiya_1734738008.jpeg', 'baba', 'baba', 1),
(3, 'Penyakit', 'Resep_Ayam_Rica_Rica_khas_Manado_oleh_Suyanti_Lie_1734737391.jpeg', 'Penyakit yang meyeramkan', 'Minum Obat', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyebab`
--

CREATE TABLE `penyebab` (
  `id_penyebab` int(11) NOT NULL,
  `nama_penyebab` text DEFAULT NULL,
  `id_admin` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `penyebab`
--

INSERT INTO `penyebab` (`id_penyebab`, `nama_penyebab`, `id_admin`) VALUES
(1, 'Virus Dengue', 1),
(2, 'sakit', 1);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indeks untuk tabel `ciri_ciri`
--
ALTER TABLE `ciri_ciri`
  ADD PRIMARY KEY (`id_ciri_ciri`),
  ADD KEY `id_penyakit` (`id_penyakit`),
  ADD KEY `id_gejala` (`id_gejala`);

--
-- Indeks untuk tabel `detail_penyebab`
--
ALTER TABLE `detail_penyebab`
  ADD PRIMARY KEY (`id_detail_penyebab`),
  ADD KEY `id_penyakit` (`id_penyakit`),
  ADD KEY `id_penyebab` (`id_penyebab`);

--
-- Indeks untuk tabel `gejala`
--
ALTER TABLE `gejala`
  ADD PRIMARY KEY (`id_gejala`),
  ADD KEY `id_admin` (`id_admin`);

--
-- Indeks untuk tabel `penyakit`
--
ALTER TABLE `penyakit`
  ADD PRIMARY KEY (`id_penyakit`),
  ADD KEY `id_admin` (`id_admin`);

--
-- Indeks untuk tabel `penyebab`
--
ALTER TABLE `penyebab`
  ADD PRIMARY KEY (`id_penyebab`),
  ADD KEY `id_admin` (`id_admin`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `ciri_ciri`
--
ALTER TABLE `ciri_ciri`
  MODIFY `id_ciri_ciri` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `detail_penyebab`
--
ALTER TABLE `detail_penyebab`
  MODIFY `id_detail_penyebab` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `gejala`
--
ALTER TABLE `gejala`
  MODIFY `id_gejala` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `penyakit`
--
ALTER TABLE `penyakit`
  MODIFY `id_penyakit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `penyebab`
--
ALTER TABLE `penyebab`
  MODIFY `id_penyebab` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `ciri_ciri`
--
ALTER TABLE `ciri_ciri`
  ADD CONSTRAINT `ciri_ciri_ibfk_1` FOREIGN KEY (`id_penyakit`) REFERENCES `penyakit` (`id_penyakit`),
  ADD CONSTRAINT `ciri_ciri_ibfk_2` FOREIGN KEY (`id_gejala`) REFERENCES `gejala` (`id_gejala`);

--
-- Ketidakleluasaan untuk tabel `detail_penyebab`
--
ALTER TABLE `detail_penyebab`
  ADD CONSTRAINT `detail_penyebab_ibfk_1` FOREIGN KEY (`id_penyakit`) REFERENCES `penyakit` (`id_penyakit`),
  ADD CONSTRAINT `detail_penyebab_ibfk_2` FOREIGN KEY (`id_penyebab`) REFERENCES `penyebab` (`id_penyebab`);

--
-- Ketidakleluasaan untuk tabel `gejala`
--
ALTER TABLE `gejala`
  ADD CONSTRAINT `gejala_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Ketidakleluasaan untuk tabel `penyakit`
--
ALTER TABLE `penyakit`
  ADD CONSTRAINT `penyakit_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Ketidakleluasaan untuk tabel `penyebab`
--
ALTER TABLE `penyebab`
  ADD CONSTRAINT `penyebab_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
