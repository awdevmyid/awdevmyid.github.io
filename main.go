func main() {
	mux := http.NewServeMux()


	mux.Handle("/", http.RedirectHandler("https://www.awdev.my.id", http.StatusSeeOther))


	http.ListenAndServe(":6000", mux)
}
