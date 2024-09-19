/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : localhost:3306
 Source Schema         : kgllm

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 19/09/2024 18:24:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_users_username`(`username` ASC) USING BTREE,
  INDEX `ix_users_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'Birdy', '$2b$12$dYPkPxlhffQmOI.LJvYMEOW1LvoPdi2Pk47Ug2GdXiz7d4gMEQgCu', '123456789@qq.com');
INSERT INTO `users` VALUES (2, 'test', '$2b$12$BxzzeMklZB06Z2NWH6wc1e5CvtrcmkVnYUhGVg6MI7gsgZff4HB3e', '1111024203@qq.com');
INSERT INTO `users` VALUES (3, 'zxy', '$2b$12$N1ENMFfii3Pp2BbSGHLpT.SfQYARvu0WH9.pwsajyqvzFLLT6q8fy', '123@qq.com');

SET FOREIGN_KEY_CHECKS = 1;
