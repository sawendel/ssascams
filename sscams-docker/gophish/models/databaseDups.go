package models

import (
	"database/sql"
	"fmt"
	"hash/fnv"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var DB = CreateDBInstance()
var mu = &sync.Mutex{}

func CreateDBInstance() *sql.DB {
	DB, err := sql.Open("mysql", "testaws:pass1234@tcp(iredmail:3306)/vmail")
	if err != nil {
		fmt.Println("error haciendo el instance")
		fmt.Println(err.Error())
		panic(err)
	}
	if DB != nil {
		fmt.Println("no esta vacia")
	}
	DB.SetConnMaxIdleTime(time.Millisecond * 10)
	DB.SetMaxIdleConns(2)
	fmt.Println("Hice el instance")

	return DB
}

func CheckDuplicates(fromAddress string, toAddress string, subject string) bool {
	mu.Lock()
	h := fnv.New32a()
	h.Write([]byte(fromAddress + toAddress + subject))
	var idtemplate = h.Sum32()
	fmt.Println("checando duplicados")
	fmt.Println(fromAddress)
	fmt.Println(toAddress)
	fmt.Println(subject)
	if DB != nil {
		fmt.Println("intancia no vacia")
	}
	var duplicated int
	rows, err := DB.Query("CALL  sscams_checkduplicate(?,?,?)", fromAddress, idtemplate, idtemplate)
	fmt.Println("luego de correr el query")
	if err != nil {
		fmt.Println("dio error")
		fmt.Println(err.Error())
		panic(err.Error()) // proper error handling instead of panic in your app
	}
	fmt.Println("antes de recorrer los results del query")
	for rows.Next() {
		err2 := rows.Scan(&duplicated)
		if err2 != nil {
			duplicated = 0
		} else {
			break
		}
	}
	rows.Close()
	mu.Unlock()
	return duplicated == 1
}
