-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `Quser`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Quser` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(45) NULL,
  `Password_hash` VARCHAR(100) NULL,
  `isadmin` INT(2) NULL DEFAULT 0,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Qquiz`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Qquiz` (
  `idquiz` INT NOT NULL AUTO_INCREMENT,
  `quiznavn` VARCHAR(45) NULL,
  `quizkategori` VARCHAR(45) NULL,
  PRIMARY KEY (`idquiz`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Qquestions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Qquestions` (
  `questionid` INT NOT NULL AUTO_INCREMENT,
  `idquiz` INT NOT NULL,
  `question` VARCHAR(150) NOT NULL,
  `alt1` VARCHAR(45) NULL,
  `alt2` VARCHAR(45) NULL,
  `alt3` VARCHAR(45) NULL,
  PRIMARY KEY (`questionid`),
  CONSTRAINT `fk_QMSpørsmål_QMquiz`
    FOREIGN KEY (`idquiz`)
    REFERENCES `Qquiz` (`idquiz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Qanswers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Qanswers` (
  `userID` INT NOT NULL,
  `questionid` INT NOT NULL,
  `answer` VARCHAR(45) NULL,
  `godkjent` INT(2) NULL DEFAULT 0,
  `kommentar` VARCHAR(100) NULL,
  PRIMARY KEY (`userID`, `questionid`),
  INDEX `fk_Qanswers_Qquestions1_idx` (`questionid` ASC) VISIBLE,
  CONSTRAINT `fk_QManswers_QMUser1`
    FOREIGN KEY (`userID`)
    REFERENCES `Quser` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Qanswers_Qquestions1`
    FOREIGN KEY (`questionid`)
    REFERENCES `Qquestions` (`questionid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Qquizcomplete`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Qquizcomplete` (
  `userID` INT NOT NULL,
  `idquiz` INT NOT NULL,
  `godkjent` INT(2) NULL DEFAULT 0,
  `kommentar` VARCHAR(100) NULL,
  PRIMARY KEY (`userID`, `idquiz`),
  INDEX `fk_Qquizcomplete_Qquiz1_idx` (`idquiz` ASC) VISIBLE,
  CONSTRAINT `fk_Qquizcomplete_Quser1`
    FOREIGN KEY (`userID`)
    REFERENCES `Quser` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Qquizcomplete_Qquiz1`
    FOREIGN KEY (`idquiz`)
    REFERENCES `Qquiz` (`idquiz`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
