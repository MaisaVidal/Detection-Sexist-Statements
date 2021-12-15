PROJECT_ID=detection-sexist-statements
#make- deploy
deploy:
	gcloud beta functions deploy event-new-detect-sexism-created \
		--project ${PROJECT_ID} \
		--runtime python39 \
		--trigger-topic topic-new-detect-sexism-created \
		--entry-point initial_method \
		--memory 512MB \
		--timeout 50s