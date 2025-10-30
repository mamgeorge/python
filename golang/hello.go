/* cd training\spring | go run hello.go

	cd training\spring go
	run hello.go

	go mod init mlgmod

	go get github.com/PaesslerAG/jsonpath@latest
	go get github.com/ohler55/ojg/jp@latest
	go get github.com/ohler55/ojg/oj@latest

	go get github.com/lib/pq
	go get github.com/godror/godror
	go get github.com/go-sql-driver/mysql
	go get github.com/mattn/go-sqlite3@latest
	go get go.mongodb.org/mongo-driver/mongo			// some examples used v2!
	go get go.mongodb.org/mongo-driver/mongo/options
	go get go.mongodb.org/mongo-driver/mongo/readpref
	go get github.com/aws/aws-sdk-go-v2/config
	go get github.com/aws/aws-sdk-go-v2/service/s3
	go get github.com/jackc/pgx/v5/stdlib
*/

package main

import ( "fmt"; "strings"; "os"; "io/ioutil"; "time"; "log"; )
import ( "encoding/json"; "net/http"; "database/sql"; )
import (  "github.com/PaesslerAG/jsonpath"; "github.com/ohler55/ojg/jp"; "github.com/ohler55/ojg/oj" )
import (
	_ "github.com/lib/pq"
//	_ "github.com/godror/godror"		// gcc issue
	_ "github.com/go-sql-driver/mysql"
//	_ "github.com/mattn/go-sqlite3"		// gcc issue

	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/bson"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"

	_ "github.com/jackc/pgx/v5/stdlib"
)

// import "C"

	const EOL = "\n"
	const TAB = "\t"
	const PI = 3.141592654
	const (
		Reset  = "\033[0m"
		Red    = "\033[31m"
		Green  = "\033[32m"
		Yellow = "\033[33m"
		Blue   = "\033[34m"
	)
	var name = "Martin"
	var arri = []int{1,2,3,4,5}
	var arrs = []string{ "Martin", "Mary", "Samuel", "Kenizie"}
	var arrq = append(arri, arri...)

func main() {

	varsys(10)

	if (false) {

		varops()
		varsys(100)
		ifcond(10)
		fmt.Println(EOL + "recurs"); fmt.Print(TAB); recurs(1)
		fmt.Println(EOL + "factor"); fmt.Print(TAB); fmt.Println(factor(9))
		mapper()
		fmt.Println(EOL + "struct"); var pers Person; pers.name = "Martin"; fmt.Println(TAB, pers)

		fmt.Println(fileIo("tmp_user.json"))
		fmt.Println(jsonPath("tmp_user.json"))

		dbPostgreSQL()	// WORKS!
		dbOracle()		// NOPE
		dbMySQL()		// NOPE
		dbSQLite()		// NOPE
		dbMongoDB()		// WORKS!
		dbAWS_S3()		// NOPE
		dbAWS_RDS()		// WORKS!

		webServer()
		webCaller()
	}

	fmt.Println(EOL + "DONE!")
}

func dbAWS_RDS() {

	fmt.Println(EOL + "dbAWS_RDS")

	var DB_HOST string = "django-pgs.cmivhxqxeajf.us-east-2.rds.amazonaws.com"
	var DB_PORT int	   = 5432
	var DB_USER string = os.Getenv("POSTGRES_USER")
	var DB_PASS string = os.Getenv("POSTGRES_PASS_RDS")
	var DB_NAME string = "initialdb"
	var DB_SQLS string = "SELECT * FROM startup_member"

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s",
		DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

	db, err := sql.Open("pgx", psqlInfo )
		if err != nil { fmt.Printf("ERROR Scan: %v\n", err) }
		defer db.Close()
		db.Ping()
		fmt.Println("Connected!")

	rows, err := db.Query(DB_SQLS)
		if err != nil { fmt.Printf("ERROR Scan: %v\n", err) }
		defer rows.Close()

	cols, err := rows.Columns();
		if err != nil { fmt.Printf("ERROR Scan: %v\n", err) }

	var results []map[string]interface{}
	for rows.Next() {

		pointers := make([]interface{}, len(cols))
		values := make([]interface{}, len(cols))
		for ictr := range values { pointers[ictr] = &values[ictr] }

		err := rows.Scan(pointers...)
			if err != nil { fmt.Printf("ERROR Scan: %v\n", err) }

		rowMap := make(map[string]interface{}, len(cols))

		for jctr, colName := range cols {
			val := *(pointers[jctr].(*interface{}))
			rowMap[colName] = val
		}

		results = append(results, rowMap)
	}

	for rctr, row := range results {
		fmt.Printf(EOL + TAB + "Row %02d:", rctr+1 )
		for key, val := range row { fmt.Printf("%-10s: %-10v", key, val) }
	}
}

func dbAWS_S3() {	// NOPE

	fmt.Println(EOL + "dbAWS_S3")

	var bucketName  string = "mlg-s3-sample"
	var bucketRegion = "us-east-2"

	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(bucketRegion),)
		if err != nil { fmt.Printf("ERROR cfg: %v\n", err) }

	s3Client := s3.NewFromConfig(cfg)

	// input := &s3.ListObjectsV2Input{ Bucket: aws.String(bucketName), Prefix: aws.String(prefix), }

	resp, err := s3Client.ListObjectsV2(context.TODO(),  &s3.ListObjectsV2Input{ Bucket: aws.String(bucketName), } )
		if err != nil { fmt.Printf("ERROR lst: %v\n", err) }

	for _, object := range resp.Contents { fmt.Printf(" - %s\n", *object.Key) }

	for _, item := range resp.Contents { fmt.Printf("key: %s, size: %d, modified: %s\n", *item.Key, item.Size, item.LastModified) }
}

func dbMongoDB() {

	fmt.Println(EOL + "dbMongoDB")

	var nameHost string = "mongodb://localhost:27017"
	var nameDatabase string = "admin"
	var nameCollection string = "employees"

	clientOptions := options.Client().ApplyURI(nameHost)

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

	client, err := mongo.Connect(ctx, clientOptions)
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }

	err = client.Ping(context.TODO(), nil)
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }

	fmt.Println("Opened MongoDB!")

	// read
	collection := client.Database(nameDatabase).Collection(nameCollection)

	filterAll := bson.D{}

	countAll, err := collection.CountDocuments(context.TODO(), filterAll)
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }

	fmt.Printf("Documents: %d\n", countAll)

	// Find many (resultMany = cursor)
	resultMany, err := collection.Find(context.TODO(), bson.D{}) // Empty filter to find all documents
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }
		defer resultMany.Close(context.TODO())

	var documentStrings []string
	for resultMany.Next(context.TODO()) {

		var rawDoc bson.Raw // Use bson.M to unmarshal into a generic map
		err := resultMany.Decode(&rawDoc)
		if err != nil { fmt.Printf("ERROR many1: %v\n", err) }

		jsonBytes, err := bson.MarshalExtJSON(rawDoc, false, false) // Convert bson.M doc to JSON
		if err != nil { fmt.Printf("ERROR many2: %v\n", err) }

		documentStrings = append(documentStrings, string(jsonBytes))
	}

	fmt.Println("\nDocuments as strings:")
	for _, docStr := range documentStrings { fmt.Println(docStr) }

	// find one
    filter := bson.M{}

    resultOne := collection.FindOne(context.TODO(), filter)

	var rawDoc bson.Raw
	err = resultOne.Decode(&rawDoc)

	jsonBytes, err := bson.MarshalExtJSON(rawDoc, false, false)
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }

	fmt.Printf("resultOne: %T %v\n", resultOne, string(jsonBytes))

	// close
	err = client.Disconnect(ctx);
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }
	fmt.Println("Closed MongoDB!")
}

func dbSQLite() {	// NOPE

	fmt.Println(EOL + "dbSQLite")
	var dbName string = "C:/workspace/dbase/sqlite/chinook.db"
	var SQL_VALS string = "SELECT id, name FROM users"

	// db, err := sql.Open("sqlite3", dbName)
	//	if err != nil { fmt.Printf("ERROR: %v\n", err) }

	// defer db.Close()
	//
	// var rows *sql.Rows
	// rows, err = db.Query(SQL_VALS)
	//	if err != nil { fmt.Printf("ERROR: %v\n", err) }
	//	defer rows.Close()
	//
	// fmt.Println(rows)
	fmt.Println(EOL + "SQL_VALS:", SQL_VALS)
	fmt.Println(EOL + "dbName: ", dbName)
}

func dbMySQL() {	// NOPE

	fmt.Println(EOL + "dbMySQL")

	var hostname string = "localhost"
	var portvals string = "3306"
	var username string = os.Getenv("MYSQL_USER")
	var password string = os.Getenv("MYSQL_PASS")
	var dataname string = "mydb"  // Optional: specify a database to connect to directly
	var SQL_VALS string = "SELECT * FROM mydb.history;"

	var conStr = username + ":" + password + "@" + "tcp(" + hostname + ":" + portvals + ")/" + dataname

	db, err := sql.Open("mysql", conStr)
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }
		defer db.Close()

	rows, _ := db.Query(SQL_VALS)
	cols, _ := rows.Columns();

	data := make(map[string]string)
	if rows.Next() {

		colPointers := make([]interface{}, len(cols))

		for cctr := range colPointers { colPointers[cctr] = &sql.NullString{} }

		rows.Scan(colPointers...)
		for qctr, val := range colPointers {

			if ( val == nil || val == "\n" ) {
				data[ cols[qctr] ] = ""
			} else {
				data[ cols[qctr] ] = val.(string)
			}
		}
    }

	fmt.Printf("%T, %v",data, data)
}

func dbOracle() {	// NOPE

	fmt.Println(EOL + "dbOracle")

	// see oracle notes: https://www.sqlpipe.com/blog/connect-to-aws-rds-with-go-d5aac

	var hostname string = "localhost"
	var portvals string= "1521"
	var username string = os.Getenv("ORACLE_USER")[0:3] // + " as sysoper"
	var password string = os.Getenv("ORACLE_PASS")
	var sid string		= "xe"  // "SYS$USERS" # aka sid or System Identifier
	var SQL_VALS string	= "SELECT * FROM employees WHERE ROWNUM <= 10 ORDER BY LAST_NAME ASC"

	dsn := username + "/" + password + "@" + hostname + ":" + portvals + "/" + sid

	//db, err := sql.Open("godror", dsn)
	//	if err != nil { fmt.Printf("ERROR: %v\n", err) }
	//	defer db.Close()

	fmt.Println(EOL + "SQL_VALS:", SQL_VALS)
	fmt.Println(EOL + "dsn: ", dsn)
}

func dbPostgreSQL() {

	fmt.Println(EOL + "dbPostgreSQL")

	var hostname string = "localhost"
	var port int = 5432
	var username string = os.Getenv("POSTGRES_USER")
	var password string = os.Getenv("POSTGRES_PASS")
	var dataname string = "dvdrental" // Optional: specify a database to connect to directly
	var SQL_VALS string = "SELECT * FROM actor LIMIT 10;"

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		hostname, port, username, password, dataname)

	db, err := sql.Open("postgres", psqlInfo);
		if err != nil { fmt.Printf("ERROR DB: %v\n", err) }
		defer db.Close()

	fmt.Printf(EOL + TAB + "Connected to: %v\n", dataname)

	rows, err := db.Query(SQL_VALS);
		if err != nil { fmt.Printf("ERROR ROWS: %v\n", err) }
		defer rows.Close()

	cols, err := rows.Columns();
		if err != nil { fmt.Printf("ERROR COLS: %v\n", err) }

	var results []map[string]interface{}
	for rows.Next() {

		pointers := make([]interface{}, len(cols))
		values := make([]interface{}, len(cols))

		for ictr := range values { pointers[ictr] = &values[ictr] }

		if err := rows.Scan(pointers...);
			err != nil { fmt.Printf("ERROR LOOP: %v\n", err) }

		rowMap := make(map[string]interface{}, len(cols))

		for jctr, colName := range cols {
			val := *(pointers[jctr].(*interface{}))
			rowMap[colName] = val
		}

		results = append(results, rowMap)
	}

	for rctr, row := range results {
		fmt.Printf(EOL + TAB + "Row %02d:", rctr+1 )
		for key, val := range row { fmt.Printf("%-10s: %-10v", key, val) }
	}
}

func webCaller() {

	fmt.Println(EOL + "webCaller")

	var link string = "https://jsonplaceholder.typicode.com/users/1"
	var resp *http.Response // "*" means resp is a pointer to http.Response struct
	var errHttp error

	resp, errHttp = http.Get(link)
	if errHttp != nil { log.Fatal(errHttp) }
	defer resp.Body.Close()

	var body [] byte
	var errBody error
	body, errBody = ioutil.ReadAll(resp.Body)
	if errBody != nil { log.Fatal(errBody) }

	fmt.Printf("Response:\n%s\n", body)
}

func webServer() {

	var port string  = ":8080"
	fmt.Println(EOL + "webServer");

	http.HandleFunc("/", webHandler) // Register the handler for the root path
	log.Printf("Server on port: %v" + EOL, port)
	log.Fatal( http.ListenAndServe(port, nil) )
}

func webHandler(rsp http.ResponseWriter, req *http.Request) {

	var now time.Time = time.Now().UTC()
	var iso string = now.Format(time.RFC3339)

	// <link rel = "icon" type = "image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=">
	var txt string = `
		<style>body { color: green; font-family: verdana; margin: auto; text-align: center; }</style>
		<br />%v
		<br />%v
		<br /><h3>Hello World from Go!</h3>`

	log.Printf(TAB + "datetime: %v" + EOL, iso)
	fmt.Fprintf(rsp, txt, now, iso)
}

func jsonPath(filePath string) string {

	fmt.Println(EOL + "jsonPath");

	// load file

		var jsonFile []uint8
		var errFile error
		jsonFile, errFile = os.ReadFile(filePath)
		if errFile != nil { fmt.Printf("ERROR: %v\n", errFile) }

	var query string = "$.company.name"

	// one way

		var jIfc map[string]interface{}
		errFile = json.Unmarshal(jsonFile, &jIfc)
		if errFile != nil { fmt.Printf("ERROR: %v\n", errFile) }

		var resultIfc interface {}
		var errJson error
		resultIfc, errJson = jsonpath.Get(query, jIfc )
		if errJson != nil { fmt.Printf("ERROR: %v\n", errJson) }
		fmt.Printf("resultIfc: %v\n", resultIfc);

	// another

		jobj, errFile := oj.ParseString( string(jsonFile) )
		if errFile != nil { fmt.Printf("ERROR: %v\n", errFile) }

		jpth, errJson := jp.ParseString(query)
		if errJson != nil { fmt.Printf("ERROR: %v\n", errJson) }

		resultXpt := jpth.Get(jobj)[0]
		fmt.Printf("resultXpt: %v\n", resultXpt);

	return resultIfc.(string)
}

func fileIo(filePath string) string {

	var content []uint8
	var errFile error

	content, errFile = os.ReadFile(filePath)
	if errFile != nil { fmt.Printf("ERROR: %v\n", errFile) }

	fmt.Println(EOL + "fileio");
	return string(content)
}

func mapper() {

	fmt.Println(EOL + "mapper");
	var mapee = map[string]string{ "name": "Martin", "age": "30", "job": "Coder", "salary": "150000" }

	fmt.Printf(TAB + "%v" + EOL + EOL, mapee)
	for k, v := range mapee { fmt.Printf(TAB + "%v : %v, " + EOL, k, v) }

	fmt.Print(EOL)
	var order = []string{ "name", "job", "salary", "age" }
	for _, v := range order { fmt.Printf(TAB + "%v : %v, " + EOL, v, mapee[v]) }
}

func factor(x float64) (y float64) {

	// factorial
	if (x > 0) { y = x * factor(x-1) } else
	{ y = 1 }
	return
}

func recurs(x int) int {

	if x == 11 { return 0 }

	fmt.Print(x, " ")
	return recurs(x + 1)
}

func ifcond(time int) {

	fmt.Println(EOL + "ifcond");

	if ( time < 18 ) { fmt.Println(TAB + "Good day.") } else
	{ fmt.Println(TAB + "Good eve.") }
}

func varsys(limit int) {

	fmt.Println(EOL + "varsys");

	var now time.Time = time.Now().UTC()
	var iso string = now.Format(time.RFC3339)
	fmt.Printf(TAB + "now: %v\n", now)
	fmt.Printf(TAB + "iso: %v\n", iso)

	fmt.Println()

	userVar := os.Getenv("USERNAME")
	fmt.Printf(TAB + "userVar: %T, %v\n" + EOL, userVar, userVar)

	if ( limit > len( os.Environ() ) ) { limit = len( os.Environ() ) }
	envVars := os.Environ()[0:limit]
	fmt.Printf(TAB + "envVars: %T, %v\n" + EOL, envVars, envVars[0])

	for num, env := range envVars {

		var dlm = strings.Index(env, "=")
		var key = env[ 0 : dlm ]
		var val = env[ dlm+1 : len(env) ]
		if ( len(val) > 60 ) { val = val[0:60] + "..." }
		fmt.Printf("\t%02d %-20s %s\n", num, key, val)
	}
}

func varops() {

	fmt.Println(EOL + "varops");

    fmt.Println(TAB + "Hello World!")
    fmt.Println(TAB + "Hello", name, "/", PI)
	fmt.Printf(TAB + "name has value: %v, and type: %T" + EOL, name, name)
	fmt.Printf(TAB + "PI has value: %v, and val: %.5v" + EOL, PI, PI)
	fmt.Printf(TAB + "arri: %v, len: %v" + EOL, arri, len(arri))
	fmt.Printf(TAB + "arrs: %v & %v\n" + EOL, arrs[0], arrs[1])
	fmt.Printf(TAB + "arrq: %v & %v & %v" + EOL, arrq, len(arrq), cap(arrq))

	for i:=0; i < 5; i++ { fmt.Print( arri[i] ) }
	fmt.Println("")

	for idx, val := range arrs { fmt.Printf(TAB + "%v\t%v" + EOL, idx, val) }
}

type Person struct {

  name string
  age int
  job string
  salary int
}
//----